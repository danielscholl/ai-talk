# Agents Creating Agents

A comprehensive look at the creation of single-file agents using Azure OpenAI SDK with a focus on Agent patterns. 

## Overview

This repository contains examples demonstrating various features of the Azure OpenAI SDK, with a focus on building intelligent agents and assistants. Each example is implemented as a self-contained Python script with built-in tests.

## Key Features Demonstrated

- Multi-agent collaboration using Azure OpenAI
- Coordinator agent delegating tasks to specialist agents
- Coordinator agent delegating tasks to specialist agents
- Basic single-agent example using Azure OpenAI
- Manager agent delegating tasks to specialized worker agents
- Customizable instructions for agents
- Error handling and response formatting with rich
- Comprehensive tests for validation

## Tutorial

1. Configure Azure OpenAI credentials by setting environment variables:

   The Evaluator (uses Azure OpenAI SDK directly):
   ```bash
   export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
   export AZURE_OPENAI_API_KEY="your_api_key"
   export AZURE_OPENAI_VERSION="2024-12-01-preview"
   ```

   The Coder (uses Aider which expects different variable names):
   ```bash
   export AZURE_API_BASE="https://your-resource.openai.azure.com"  
   export AZURE_API_KEY="your_api_key"
   export AZURE_API_VERSION="2024-12-01-preview"
   ```

   For other providers, set the following environment variables:
   ```bash
   export OPENAI_API_KEY="your_api_key"
   export ANTHROPIC_API_KEY="your_api_key"
   ```

2. Initialize the Project

   ```bash
   uv sync
   ```

2. Use the Director to create an agent.

   __Basic Agent__
   ```bash
   uv run python director.py --config specs/director_basic_agent_maker.yaml
   uv run python director.py --config specs/director_multi_agent_maker.yaml
   ```

## Using a Pull Request Description Agent

1. Install AIPR

   ```bash
   pip install pr-generator-agent
   ```

2. Analyze the Change Set

   ```bash
   aipr
   ```

## Sample Agents