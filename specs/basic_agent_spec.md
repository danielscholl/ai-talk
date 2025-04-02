# Basic Azure OpenAI Agent Specification
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Create a simple, single-file agent that calls Azure OpenAI service to respond to user prompts

## Mid-Level Objective

- Set up proper authentication using Azure OpenAI using key authentication
- Include test functions for validation
- Allow customizable instructions for the agent
- Handle command-line arguments and environment variables
- Implement error handling and proper response formatting
- Create a self-contained basic agent system with Azure OpenAI

## Implementation Notes

- The script must follow the uv run script format with shebang and dependencies declaration
- Use the exact shebang line: `#!/usr/bin/env -S uv run --script`
- Include a uv script dependencies block
- NEVER use a requirements.txt file as it won't be needed due to the uv script dependencies block
- The script and tests should be self-contained in a single file
- Support environment variables for configuration (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_VERSION)
- Include clear, concise docstrings and comments
- Default to "gpt-4o" model name for all agents
- Follow Python best practices for error handling
- Include tests that can be run with pytest
- Format responses using python rich console and panels for a better user experience
- Add the agent to the AGENTS.md file with a basic description of the agent including a mermaid sequence diagram, how to run it and execute tests

## Context

### Beginning context
- agents/AGENTS.md

### Ending context
- agents/basic_agent.py (new)
- agents/AGENTS.md (updated)

## Low-Level Tasks
> Ordered from start to finish

1. Setup script metadata and imports
```aider
CREATE agents/basic_agent.py
Add the exact shebang line: #!/usr/bin/env -S uv run --script

Add a script dependency block and update for any new dependencies:
# /// script
# dependencies = [
#   "openai-agents>=0.0.2",
#   "pytest>=7.4.0",
#   "rich>=13.7.0",
#   "azure-identity>=1.15.0",
#   "python-dotenv>=1.0.0",
# ]
# ///

Add docstrings explaining the agent's purpose and how to run it:
"""
Some Agent Example with Azure OpenAI

This agent performs (...)

Run with:
    uv run agent.py --prompt "Tell me about the origin of the Egyptian pyramids"

Test with:
    uv run pytest agent.py
```

2. Create Agent Class and Implement core functionality
```aider
UPDATE agents/basic_agent.py
    CREATE class Agent:
        - CREATE def __init__(self, name: str, instructions: str, model: str)
        - CREATE  async def run(self, prompt: str) -> str
            - retrieve a client
            - send messages to LLM using client
            - return message LLM content from client

    CREATE def get_client()
        - Check for required environment variables
        - Return a configured Azure OpenAI client

    CREATE def create_agent(instructions: str = None) -> Agent
        - Define default instructions if none provided
        - Create and configure agent with Azure OpenAI
        - Return an agent instance

    CREATE async def run_agent(prompt, agent=None)
        - Create agent if none provided
        - Run the agent with prompt provided
        - Return the content response
```

3. Implement main functionality
```aider
UPDATE agents/basic_agent.py
    CREATE def main() -> None
        - Parse command line arguments for prompt
        - Run the agent with the provided prompt aysnchronously
        - Display the response using rich console and panels.
        - Handle errors gracefully

    ADD if __name__ == "__main__" entry point
```

4. Implement synchronous tests
```aider
UPDATE agents/basic_agent.py

    CREATE def test_create_basic_agent()
        - Test agent creation with custom instructions
        - Verify agent properties (name, instructions, model, ...)

    CREATE def test_run_basic_agent()
        - Test running the agent with no mocks using a simple prompt asking:  (What is 2+2?)
        - Verify response returned is non-empty and contains expected content: (4)
```