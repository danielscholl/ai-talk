# uv run python director.py --config specs/director_basic_agent_maker.yaml
# uv run python director.py --config specs/director_multi_agent_maker.yaml

## Director is a LLM as a judge pattern.  https://www.evidentlyai.com/llm-guide/llm-as-a-judge

import shlex
from pydantic import BaseModel
from typing import Optional, List, Literal
from pathlib import Path
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
import sys
import yaml
import argparse
from openai import OpenAI, AzureOpenAI
import subprocess
import os


class EvaluationResult(BaseModel):
    success: bool
    feedback: Optional[str]


class DirectorConfig(BaseModel):
    prompt: str
    coder_model: str
    evaluator_model: Literal[
        "gpt-4o", "gpt-4o-mini", "o1-mini", "o1-preview",
        "azure/o1", "azure/o1-mini", "azure/o3-mini"
    ]
    max_iterations: int
    execution_command: str
    context_editable: List[str]
    context_read_only: List[str]
    evaluator: Literal["default"]


class Director:
    """
    Self Directed AI Coding Assistant
    """

    def __init__(self, config_path: str):
        self.config = self.validate_config(Path(config_path))
        self.llm_client = self.initialize_llm_client()

    def initialize_llm_client(self) -> OpenAI:
        """Initialize the appropriate OpenAI client based on model prefix"""
        if self.config.evaluator_model.startswith("azure/"):
            # Get deployment name by removing 'azure/' prefix
            deployment = self.get_model_name(self.config.evaluator_model)
            
            # Validate deployment name
            if not deployment or deployment == "":
                raise ValueError(f"Invalid deployment name extracted from model: {self.config.evaluator_model}")

            # Get values from AZURE_OPENAI_* environment variables
            azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            azure_version = os.getenv("AZURE_OPENAI_VERSION")

            # Check if we have the required variables
            if not azure_api_key:
                raise ValueError("AZURE_OPENAI_API_KEY environment variable is required for Azure OpenAI evaluator")
            if not azure_endpoint:
                raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is required for Azure OpenAI evaluator")
            if not azure_version:
                raise ValueError("AZURE_OPENAI_VERSION environment variable is required for Azure OpenAI evaluator")

            # Ensure endpoint has trailing slash
            if not azure_endpoint.endswith('/'):
                azure_endpoint = azure_endpoint + '/'
                os.environ["AZURE_OPENAI_ENDPOINT"] = azure_endpoint  # Update the original variable too
            
            self.file_log(f"Using Azure OpenAI with deployment: {deployment}, version: {azure_version}")
            
            return AzureOpenAI(
                api_version=azure_version,
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                azure_deployment=deployment,
            )
        else:
            return OpenAI()

    def get_model_name(self, model: str) -> str:
        """Convert model name to appropriate format based on service"""
        if model.startswith("azure/"):
            return model.replace("azure/", "", 1)
        return model

    @staticmethod
    def validate_config(config_path: Path) -> DirectorConfig:
        """Validate the yaml config file and return DirectorConfig object."""
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path) as f:
            config_dict = yaml.safe_load(f)

        # If prompt ends with .md, read content from that file
        if config_dict["prompt"].endswith(".md"):
            prompt_path = Path(config_dict["prompt"])
            if not prompt_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
            with open(prompt_path) as f:
                config_dict["prompt"] = f.read()

        config = DirectorConfig(**config_dict)

        # Validate evaluator_model is one of the allowed values
        allowed_evaluator_models = {
            "gpt-4o", "gpt-4o-mini", "o1-mini", "o1-preview",
            "azure/o1", "azure/o1-mini", "azure/o3-mini"
        }
        if config.evaluator_model not in allowed_evaluator_models:
            raise ValueError(
                f"evaluator_model must be one of {allowed_evaluator_models}, "
                f"got {config.evaluator_model}"
            )

        # Validate coder_model if it's an Azure model
        if config.coder_model.startswith("azure/"):
            allowed_azure_coder_models = {"azure/gpt-4o"}
            if config.coder_model not in allowed_azure_coder_models:
                raise ValueError(
                    f"When using Azure, coder_model must be 'azure/gpt-4o', "
                    f"got {config.coder_model}. Note: The model name must match your Azure deployment name exactly."
                )

        # Validate we have at least 1 editable file
        if not config.context_editable:
            raise ValueError("At least one editable context file must be specified")

        # Validate all paths in context_editable and context_read_only exist
        for path in config.context_editable:
            if not Path(path).exists():
                raise FileNotFoundError(f"Editable context file not found: {path}")

        for path in config.context_read_only:
            if not Path(path).exists():
                raise FileNotFoundError(f"Read-only context file not found: {path}")

        return config

    def parse_llm_json_response(self, str) -> str:
        """
        Parse and fix the response from an LLM that is expected to return JSON.
        """
        if "```" not in str:
            str = str.strip()
            self.file_log(f"raw pre-json-parse: {str}", print_message=False)
            return str

        # Remove opening backticks and language identifier
        str = str.split("```", 1)[-1].split("\n", 1)[-1]

        # Remove closing backticks
        str = str.rsplit("```", 1)[0]

        str = str.strip()

        self.file_log(f"post-json-parse: {str}", print_message=False)

        # Remove any leading or trailing whitespace
        return str

    def file_log(self, message: str, print_message: bool = True):
        if print_message:
            print(message)
        with open("director_log.txt", "a+", encoding="utf-8") as f:
            f.write(message + "\n")

    # ------------- Key Director Methods -------------

    def create_new_ai_coding_prompt(
        self,
        iteration: int,
        base_input_prompt: str,
        execution_output: str,
        evaluation: EvaluationResult,
    ) -> str:
        if iteration == 0:
            return base_input_prompt
        else:
            return f"""
# Generate the next iteration of code to achieve the user's desired result based on their original instructions and the feedback from the previous attempt.
> Generate a new prompt in the same style as the original instructions for the next iteration of code.

## This is your {iteration}th attempt to generate the code.
> You have {self.config.max_iterations - iteration} attempts remaining.

## Here's the user's original instructions for generating the code:
{base_input_prompt}

## Here's the output of your previous attempt:
{execution_output}

## Here's feedback on your previous attempt:
{evaluation.feedback}"""

    def ai_code(self, prompt: str):
        # If using Azure model, set the API version in environment for aider
        original_vars = {}
        try:
            if self.config.coder_model.startswith("azure/"):
                # Store original environment variables
                original_vars = {
                    'azure_api_version': os.getenv("AZURE_API_VERSION"),
                    'azure_api_key': os.getenv("AZURE_API_KEY"),
                    'azure_api_base': os.getenv("AZURE_API_BASE"),
                    'api_type': os.getenv("OPENAI_API_TYPE"),
                    'api_version': os.getenv("OPENAI_API_VERSION"),
                    'api_base': os.getenv("OPENAI_API_BASE"),
                    'api_key': os.getenv("OPENAI_API_KEY"),
                    'deployment': os.getenv("OPENAI_DEPLOYMENT_NAME"),
                    'model': os.getenv("OPENAI_MODEL_NAME")
                }

                # Get deployment name (model name without azure/ prefix)
                deployment = self.get_model_name(self.config.coder_model)

                # Check for required AZURE_API_* variables (required by Aider)
                azure_api_key = os.getenv("AZURE_API_KEY")
                azure_endpoint = os.getenv("AZURE_API_BASE")
                azure_version = os.getenv("AZURE_API_VERSION")

                # Check if we have the required variables
                if not azure_api_key:
                    raise ValueError("AZURE_API_KEY environment variable is required for Azure OpenAI with Aider")
                if not azure_endpoint:
                    raise ValueError("AZURE_API_BASE environment variable is required for Azure OpenAI with Aider")
                if not azure_version:
                    raise ValueError("AZURE_API_VERSION environment variable is required for Azure OpenAI with Aider")

                # Ensure endpoint has trailing slash
                if not azure_endpoint.endswith('/'):
                    azure_endpoint = azure_endpoint + '/'

                self.file_log(f"Using Azure OpenAI with deployment: {deployment}, version: {azure_version}")
                
                # Set OpenAI variables as fallback
                os.environ["OPENAI_API_TYPE"] = "azure"
                os.environ["OPENAI_API_VERSION"] = azure_version
                os.environ["OPENAI_API_BASE"] = azure_endpoint
                os.environ["AZURE_API_BASE"] = azure_endpoint  # Update the original variable too
                
                model = Model(self.config.coder_model)
                coder = Coder.create(
                    main_model=model,
                    io=InputOutput(yes=True),
                    fnames=self.config.context_editable,
                    read_only_fnames=self.config.context_read_only,
                    auto_commits=False,
                    suggest_shell_commands=False,
                    detect_urls=False,
                )
                try:
                    coder.run(prompt)
                finally:
                    # Clean up resources
                    if hasattr(coder, 'cleanup'):
                        coder.cleanup()
                    # Force close any remaining event loops
                    if hasattr(model, 'close'):
                        model.close()
            else:
                # Non-Azure model
                self.file_log(f"Using model: {self.config.coder_model}")
                model = Model(self.config.coder_model)
                coder = Coder.create(
                    main_model=model,
                    io=InputOutput(yes=True),
                    fnames=self.config.context_editable,
                    read_only_fnames=self.config.context_read_only,
                    auto_commits=False,
                    suggest_shell_commands=False,
                    detect_urls=False,
                )
                try:
                    coder.run(prompt)
                finally:
                    # Clean up resources
                    if hasattr(coder, 'cleanup'):
                        coder.cleanup()
                    # Force close any remaining event loops
                    if hasattr(model, 'close'):
                        model.close()
        finally:
            # Restore original environment variables
            if self.config.coder_model.startswith("azure/"):
                for key, value in original_vars.items():
                    env_key = {
                        'azure_api_version': "AZURE_API_VERSION",
                        'azure_api_key': "AZURE_API_KEY",
                        'azure_api_base': "AZURE_API_BASE",
                        'api_type': "OPENAI_API_TYPE",
                        'api_version': "OPENAI_API_VERSION",
                        'api_base': "OPENAI_API_BASE",
                        'api_key': "OPENAI_API_KEY",
                        'deployment': "OPENAI_DEPLOYMENT_NAME",
                        'model': "OPENAI_MODEL_NAME"
                    }[key]
                    if value is not None:
                        os.environ[env_key] = value
                    else:
                        os.environ.pop(env_key, None)

    def execute(self) -> str:
        """Execute the tests and return the output as a string."""
        result = subprocess.run(
            shlex.split(self.config.execution_command),
            capture_output=True,
            text=True,
        )
        self.file_log(
            f"Execution output: \n{result.stdout + result.stderr}",
            print_message=False,
        )
        return result.stdout + result.stderr

    def evaluate(self, execution_output: str) -> EvaluationResult:
        if self.config.evaluator != "default":
            raise ValueError(
                f"Custom evaluator {self.config.evaluator} not implemented"
            )

        map_editable_fname_to_files = {
            Path(fname).name: Path(fname).read_text()
            for fname in self.config.context_editable
        }

        map_read_only_fname_to_files = {
            Path(fname).name: Path(fname).read_text()
            for fname in self.config.context_read_only
        }

        # Add JSON instruction at the start of the prompt for all models
        json_instruction = """You must respond with valid JSON only. No other text.
The JSON must match this structure exactly:
{
    "success": boolean,
    "feedback": string or null
}
"""

        evaluation_prompt = f"""{json_instruction}Evaluate this execution output and determine if it was successful based on the execution command, the user's desired result, the editable files, checklist, and the read-only files.

## Checklist:
- Is the execution output reporting success or failure?
- Did we miss any tasks? Review the User's Desired Result to see if we have satisfied all tasks.
- Did we satisfy the user's desired result?
- Ignore warnings

## User's Desired Result:
{self.config.prompt}

## Editable Files:
{map_editable_fname_to_files}

## Read-Only Files:
{map_read_only_fname_to_files}

## Execution Command:
{self.config.execution_command}

## Execution Output:
{execution_output}

## Response Format:
> Be 100% sure to output JSON.parse compatible JSON.
> That means no new lines.

Return a structured JSON response with the following structure: {{
    success: bool - true if the execution output generated by the execution command matches the Users Desired Result
    feedback: str | None - if unsuccessful, provide detailed feedback explaining what failed and how to fix it, or None if successful
}}"""

        self.file_log(
            f"Evaluation prompt: ({self.config.evaluator_model}):\n{evaluation_prompt}",
            print_message=False,
        )

        try:
            model_name = self.get_model_name(self.config.evaluator_model)
            
            # Create the completion - response_format is only supported by certain models
            # For now, we'll use it only in the fallback case with gpt-4o
            completion = self.llm_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": evaluation_prompt}]
            )

            self.file_log(
                f"Evaluation response: ({self.config.evaluator_model}):\n{completion.choices[0].message.content}",
                print_message=False,
            )

            evaluation = EvaluationResult.model_validate_json(
                self.parse_llm_json_response(completion.choices[0].message.content)
            )

            return evaluation
        except Exception as e:
            self.file_log(
                f"Error evaluating execution output for '{self.config.evaluator_model}'. Error: {e}. Falling back to gpt-4o & structured output."
            )

            ## Fallback using standard OpenAI client with gpt-4o which supports response_format
            fallback_client = OpenAI()  # Create new standard OpenAI client for fallback
            try:
                completion = fallback_client.beta.chat.completions.parse(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": evaluation_prompt,
                        },
                    ],
                    response_format=EvaluationResult,
                )

                message = completion.choices[0].message
                if message.parsed:
                    return message.parsed
                else:
                    raise ValueError("Failed to parse the response")
            except Exception as fallback_error:
                raise ValueError(f"Both primary and fallback evaluation failed. Primary error: {e}, Fallback error: {fallback_error}")

    def direct(self):
        try:
            evaluation = EvaluationResult(success=False, feedback=None)
            execution_output = ""
            success = False

            for i in range(self.config.max_iterations):
                self.file_log(f"\nIteration {i+1}/{self.config.max_iterations}")

                self.file_log("🧠 Creating new prompt...")
                new_prompt = self.create_new_ai_coding_prompt(
                    i, self.config.prompt, execution_output, evaluation
                )

                self.file_log("🤖 Generating AI code...")
                self.ai_code(new_prompt)

                self.file_log(f"💻 Executing code... '{self.config.execution_command}'")
                execution_output = self.execute()

                self.file_log(
                    f"🔍 Evaluating results... '{self.config.evaluator_model}' + '{self.config.evaluator}'"
                )
                evaluation = self.evaluate(execution_output)

                self.file_log(
                    f"🔍 Evaluation result: {'✅ Success' if evaluation.success else '❌ Failed'}"
                )
                if evaluation.feedback:
                    self.file_log(f"💬 Feedback: \n{evaluation.feedback}")

                if evaluation.success:
                    success = True
                    self.file_log(
                        f"\n🎉 Success achieved after {i+1} iterations! Breaking out of iteration loop."
                    )
                    break
                else:
                    self.file_log(
                        f"\n🔄 Continuing with next iteration... Have {self.config.max_iterations - i - 1} attempts remaining."
                    )

            if not success:
                self.file_log(
                    "\n🚫 Failed to achieve success within the maximum number of iterations."
                )

            self.file_log("\nDone.")
        finally:
            # Clean up any remaining resources
            if hasattr(self.llm_client, 'close'):
                self.llm_client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the AI Coding Director with a config file"
    )
    parser.add_argument(
        "--config",
        type=str,
        default="specs/basic.yaml",
        help="Path to the YAML config file",
    )
    args = parser.parse_args()
    director = Director(args.config)
    director.direct()
