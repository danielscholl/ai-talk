#!/usr/bin/env bash
#
# PLAN-EXECUTE PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Using a "plan prompt" to develop a strategic approach
#  2) Using an "execute prompt" to implement the plan
#
# This pattern separates reasoning/planning from execution for more 
# structured and thoughtful results.

########################################
# TASK DEFINITION
########################################
# Single focused task that showcases the power of planning before execution
TASK="Design a comprehensive AI system that can analyze customer support tickets, categorize issues, suggest solutions, and identify emerging patterns to improve product design"

echo "---------------------"
echo "🔍 PLAN-EXECUTE PROMPT PATTERN DEMO"
echo "---------------------"
echo "Task to be completed:"
echo "$TASK"
echo "---------------------"

########################################
# 1. PLANNING PHASE
# 
# The planning prompt develops a strategic approach
# before any implementation begins
########################################
PLAN_PROMPT="You are a strategic AI systems architect.
For the following complex task, develop a detailed, step-by-step plan. 
Focus on creating a comprehensive technical approach that addresses all key aspects.
Do not implement any part of the plan yet - just create the architectural blueprint.

TASK: $TASK

Respond with a clear, numbered plan with 5-7 main components.
For each component, include:
1. The purpose and functionality of this component
2. Key technical considerations or requirements
3. How it interfaces with other components
4. Success criteria for this component

Format your response as a plan only, without any introduction or conclusion."

echo "🧩 Phase 1: Generating strategic plan..."
PLAN=$(llm "$PLAN_PROMPT")

# Display the plan
echo "---------------------"
echo "📋 STRATEGIC PLAN:"
echo "---------------------"
echo "$PLAN"
echo "---------------------"

########################################
# 2. EXECUTION PHASE
# 
# The execution prompt implements the plan
# that was created in the planning phase
########################################
EXECUTE_PROMPT="You are a technical implementation specialist.
Using the strategic architectural plan below, provide a detailed technical implementation.
Follow the system architecture exactly but fill in all necessary technical details for practical execution.

SYSTEM ARCHITECTURE PLAN:
$PLAN

TASK: $TASK

Your implementation should:
1. Follow each component of the architecture in order
2. Provide specific, actionable technical details for each component
3. Include sample code snippets, API specifications, or data schemas where appropriate
4. Specify technologies, frameworks, and tools to be used
5. Address potential technical challenges and their solutions

Format your response with clear sections corresponding to each component in the plan."

echo "🔨 Phase 2: Executing the plan..."
IMPLEMENTATION=$(llm "$EXECUTE_PROMPT")

# Display the implementation
echo "---------------------"
echo "🚀 IMPLEMENTATION:"
echo "---------------------"
echo "$IMPLEMENTATION"
echo "---------------------"

echo "✅ Plan-Execute prompt pattern demonstration complete!"
echo "This pattern promotes methodical problem-solving by ensuring"
echo "thorough planning before implementation, reducing errors and"
echo "improving the overall quality of complex technical systems."
exit 0