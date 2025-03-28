# Azure OpenAI SDK Examples

A comprehensive collection of single-file examples showcasing the capabilities of the Azure OpenAI SDK with a focus on Agent patterns.


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

## Setup

1. Configure Azure OpenAI credentials by either:

   Creating a .env file:
   ```bash
   cp .env_sample .env
   # Edit .env with your values
   ```

   Or setting environment variables directly:
   ```bash
   export AZURE_API_KEY="your_api_key"
   export AZURE_API_BASE="https://your-resource.openai.azure.com/"
   ```

2. Use the Director to create an agent.

   __Basic Agent__
   ```bash
   uv run python director.py --config specs/director_basic_agent_maker.yaml
   
   ```

# Agent Descriptions
