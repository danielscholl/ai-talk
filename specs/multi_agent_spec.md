# Multi Agent Specification using Azure OpenAI
> Ingest the information from this file, implement the Low-Level Tasks, and generate the code that will satisfy the High and Mid-Level Objectives.

## High-Level Objective

- Create a multi-agent system utilizing Azure OpenAI service with a coordinator agent responsible for delegating tasks to specialist agents based on query topic.

## Mid-Level Objective

- Set up proper authentication using Azure OpenAI using key authentication
- Include test functions for validation
- Allow customizable instructions for the agent
- Handle command-line arguments and environment variables
- Implement error handling and proper response formatting
- Create a self-contained multi-agent system with Azure OpenAI
- Implement specialist agents with domain-specific knowledge
- Create a coordinator agent that delegates to specialists

## Implementation Notes

- The script must follow the uv run script format with shebang and dependencies declaration
- Use the exact shebang line: `#!/usr/bin/env -S uv run --script`
- Include the uv script dependencies block exactly as provided
- NEVER use a requirements.txt file as it won't be needed due to the uv script dependencies block
- The script and tests should be self-contained in a single file
- Support environment variables for configuration (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY, AZURE_OPENAI_VERSION)
- Include clear, concise docstrings and comments
- Default to "gpt-4o" model name for all agents
- Follow Python best practices for error handling
- Include tests that can be run with pytest
- Format responses using python rich console and panels for a better user experience
- Add the agent to the AGENTS.md file with a basic description of the agent including a mermaid sequence diagram, how to run it and execute tests
- Coordinator must detect when to delegate using keyword detection
- Specialist must provide a response from the Coordinator

## Context

### Beginning context
- agents/AGENTS.md

### Ending context
- agents/multi_agent.py (new)
- agents/AGENTS.md (updated)

## Low-Level Tasks
> Ordered from start to finish

1. Setup script metadata and imports
```aider
CREATE agents/multi_agent.py
Add the exact shebang line: #!/usr/bin/env -S uv run --script

Add the exact script dependency block DO NOT add dependencies:
# /// script
# dependencies = [
#   "pytest>=7.4.0",
#   "rich>=13.7.0",
#   "azure-identity>=1.15.0",
#   "python-dotenv>=1.0.0",
#   "openai>=1.65.0,<1.66.0"
# ]
# ///

Add a docstring explaining the agent's purpose and how to run it:
"""
Some Agent Example with Azure OpenAI

This agent does (...)

Run with:
    uv run agent.py --prompt "Explain quantum computing and its applications"

Test with:
    uv run pytest agent.py
```

2. Implement core client and data structure functionality
```aider
UPDATE agents/multi_agent.py
    CREATE def get_client() -> AzureOpenAI
        - Check for required environment variables (AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_KEY)
        - Use default API version if not specified (2024-12-01-preview)
        - Return configured client

    CREATE @dataclass Handoff
        - Define a dataclass for handoffs between agents
        - Include agent reference and description fields
```

3. Implement the Agent class
```aider
UPDATE agents/multi_agent.py
    CREATE class Agent
        - CREATE def __init__(
            self,
            name: str,
            instructions: str,
            model: str = str,
            handoffs: List[Handoff] = None,
            handoff_description: Optional[str] = None
        )
        - CREATE async def run(self, prompt: str) -> str
          - Build full instructions including handoff options if available
          - Retrieve a client
          - Check for handoffs
          - Create messages
          - Send Messages to LLM
          - Check for delegation directives in the response
          - Delegate to specialist agents as necessary
          - Return the final response
```

4. Implement utility functions and specialist agents
```aider
UPDATE agents/multi_agent.py
    CREATE def handoff(agent: Agent, description: Optional[str] = None) -> Handoff
        - Create a Handoff object to the specified agent
        - Use provided description or agent handoff_description

    CREATE def create_science_agent() -> Agent
        - DEFINE instructions for science specialist
            "You are a science specialist with deep knowledge of physics, chemistry, biology, and related fields.
            Provide accurate, detailed scientific explanations while making complex concepts accessible.
            Use analogies and examples when helpful to illustrate scientific principles.
            Always clarify when something is theoretical or not yet proven.
            All replies should be in an essay format appropriate for school."
        - Create and return Agent with science focus and appropriate handoff description

    CREATE def create_tech_agent() -> Agent
        - DEFINE instructions for technology specialist
            "You are a technology specialist with expertise in computer science, programming, AI, and digital technologies.
            Provide clear, accurate explanations of technical concepts and their practical applications.
            When discussing programming, focus on concepts rather than writing extensive code.
            Explain how technologies work and their real-world impact.
            All replies should be in JSON format."
        - Create and return Agent with technology focus and appropriate handoff description

    CREATE def create_coordinator_agent(specialists: List[Agent]) -> Agent
        - DEFINE instructions for coordinator agent
            "You are a coordinator who determines which specialist should handle a user's question.
            Analyze the user's query and decide which specialist would be best suited to respond.
            For questions that span multiple domains, choose the specialist most relevant to the core of the question.
            Always delegate to a specialist rather than answering yourself."
        - Create handoffs to all specialist agents
        - Create and return Agent with coordination focus and handoffs
```

5. Implement the multi-agent system runner
```aider
UPDATE agents/multi_agent.py
    CREATE async def run_multi_agent_system(prompt: str) -> str
        - Create specialist agents (science and tech)
        - Create coordinator agent with specialists
        - Run the coordinator agent with the prompt
        - Display the coordinator decision process using a special rich panel.
        - Return the final response from the system
```

6. Implement main functionality and CLI interface
```aider
UPDATE agents/multi_agent.py
    CREATE def main() -> None
        - Parse command line arguments for prompt
        - Run the agent with the provided prompt aysnchronously
        - Display the response using rich panels.
        - Handle errors gracefully

    ADD if __name__ == "__main__" entry point to call main()
```

4. Implement synchronous tests only
```aider
UPDATE agents/multi_agent.py
    CREATE def test_create_specialist_agents()
        - Test that specialist agents are created with the correct configuration.
        - Create science and tech specialist agents
        - Verify their names, instructions, and model settings

    CREATE def test_create_coordinator_agent()
        - Test that the coordinator agent is created with the correct configuration.
        - Create specialist agents
        - Create coordinator agent with specialists
        - Verify coordinator name, instructions, and handoffs

    CREATE def test_handoff_function()
        - Test the handoff function.
        - Create an agent
        - Create a handoff to the agent
        - Verify the handoff agent and description match expectations

    CREATE def test_run_multi_agent_system()
        - Test that the multi-agent system can run and produce a valid response.
        - Use asyncio.run and verify a simple test query that should go to the tech specialist
```
