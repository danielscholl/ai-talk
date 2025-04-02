#!/bin/bash
#
# WORKERS PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Using a planning prompt to break a task into subtasks
#  2) Delegating subtasks to specialized "worker" prompts
#  3) Using a synthesis prompt to combine the worker outputs
#
# This pattern enables parallel, specialized processing of complex tasks,
# similar to a team of specialists coordinated by a project manager.

########################################
# TASK DEFINITION
########################################
# The main task that will be divided into subtasks
MAIN_TASK="generating a talk on AI"

echo "---------------------"
echo "🔄 WORKERS PROMPT PATTERN DEMO"
echo "---------------------"
echo "Main task: $MAIN_TASK"
echo "---------------------"

########################################
# 1. PLANNING PHASE
# 
# Break the main task into distinct subtasks
########################################
echo "📋 Phase 1: Planning the task..."
PLAN=$(llm --model gpt-4o-mini "Create a plan with three subtasks for $MAIN_TASK. Each subtask should be specialized and distinct.")

# Display the plan
echo "---------------------"
echo "Plan:"
echo "$PLAN"
echo "---------------------"

# Extract the subtasks from the plan
SUBTASKS=$(llm --model gpt-4o-mini "Extract the three subtasks from this plan:\n$PLAN")

# Split the subtasks into individual tasks
TASK1=$(llm --model gpt-4o-mini "From the following list, return only subtask 1:\n$SUBTASKS")
TASK2=$(llm --model gpt-4o-mini "From the following list, return only subtask 2:\n$SUBTASKS")
TASK3=$(llm --model gpt-4o-mini "From the following list, return only subtask 3:\n$SUBTASKS")

# Display the individual tasks
echo "Subtask 1: $TASK1"
echo "Subtask 2: $TASK2"
echo "Subtask 3: $TASK3"
echo "---------------------"

########################################
# 2. WORKER EXECUTION PHASE
# 
# Each "worker" completes its specialized subtask
########################################
echo "👷 Phase 2: Executing specialized workers..."

echo "Worker 1 processing..."
RESULT1=$(llm --model gpt-4 "You are a specialized worker focused on this specific task.
Complete this subtask thoroughly and with expertise:

SUBTASK: $TASK1

Provide a comprehensive, high-quality result.")

echo "Worker 2 processing..."
RESULT2=$(llm --model gpt-4 "You are a specialized worker focused on this specific task.
Complete this subtask thoroughly and with expertise:

SUBTASK: $TASK2

Provide a comprehensive, high-quality result.")

echo "Worker 3 processing..."
RESULT3=$(llm --model gpt-4 "You are a specialized worker focused on this specific task.
Complete this subtask thoroughly and with expertise:

SUBTASK: $TASK3

Provide a comprehensive, high-quality result.")

echo "All workers completed their subtasks."
echo "---------------------"

########################################
# 3. SYNTHESIS PHASE
# 
# Combine all worker outputs into a cohesive final result
########################################
echo "🧠 Phase 3: Synthesizing final output..."
FINAL=$(llm --model gpt-4o "You are a synthesis specialist.
Combine the following results from specialized workers into a cohesive, unified output.
Ensure the final result is well-structured, comprehensive, and flows naturally.

WORKER 1 RESULT (${TASK1}):
$RESULT1

WORKER 2 RESULT (${TASK2}):
$RESULT2

WORKER 3 RESULT (${TASK3}):
$RESULT3

Format the output in markdown with appropriate headings, lists, and formatting.
The result should be a complete, professional document about $MAIN_TASK.")

echo "---------------------"
echo "🚀 FINAL SYNTHESIZED OUTPUT:"
echo "---------------------"
echo "$FINAL"
echo "---------------------"

echo "✅ Workers prompt pattern demonstration complete!"
echo "This pattern breaks complex tasks into specialized subtasks,"
echo "processes them with focused workers, and synthesizes the results"
echo "for higher quality and more comprehensive outputs."
exit 0
