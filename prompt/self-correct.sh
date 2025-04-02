#!/usr/bin/env bash
#
# SELF-CORRECT PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Using an initial prompt to generate content
#  2) Validating that content for errors or improvements
#  3) Self-correcting based on the validation
#  4) Repeating until validation passes or max attempts reached
#
# This pattern enables autonomous error detection and correction,
# reducing the need for human intervention.

########################################
# TASK DEFINITION
########################################
# Single focused task for demonstration purposes
TASK="Write a Python function to calculate the Fibonacci sequence up to n terms"
VALIDATION_CRITERIA="Check for correctness, efficiency, edge cases (n=0, n=1), and proper documentation"

echo "---------------------"
echo "🔄 SELF-CORRECT PROMPT PATTERN DEMO"
echo "---------------------"
echo "Task to be completed:"
echo "$TASK"
echo "Validation criteria:"
echo "$VALIDATION_CRITERIA"
echo "---------------------"

########################################
# 1. INITIAL GENERATION PHASE
# 
# Create the first version of content with an initial prompt
########################################
INITIAL_PROMPT="You are an expert creator.
Generate a solution for the following task:

TASK: $TASK

Provide a high-quality, professional solution.
Be thorough and pay attention to details."

echo "✍️ Phase 1: Generating initial solution..."
CURRENT_OUTPUT=$(llm "$INITIAL_PROMPT")

# Display the initial output
echo "---------------------"
echo "📝 INITIAL SOLUTION (Attempt 1):"
echo "---------------------"
echo "$CURRENT_OUTPUT"
echo "---------------------"

########################################
# 2. SELF-CORRECTION LOOP
# 
# Iteratively validate and improve the content
########################################
MAX_ATTEMPTS=3
ATTEMPT=1
ISSUES="Initial validation"

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  # Increment attempt counter
  ATTEMPT=$((ATTEMPT + 1))
  
  # Create validation prompt to identify issues
  VALIDATION_PROMPT="You are a critical validator.
Carefully evaluate the following solution based on the specified criteria:

SOLUTION:
$CURRENT_OUTPUT

TASK: $TASK

VALIDATION CRITERIA: $VALIDATION_CRITERIA

Identify any issues, errors, or areas for improvement. Be specific and thorough.
If the solution is perfect and meets all criteria, respond with only the word 'VALID'.
Otherwise, list each issue clearly and concisely, one per line."

  echo "🔍 Validating solution (Attempt $((ATTEMPT-1)))..."
  VALIDATION_RESULT=$(llm "$VALIDATION_PROMPT")
  
  # Check if validation passed
  if [ "$VALIDATION_RESULT" = "VALID" ]; then
    echo "✅ Validation passed! No issues found."
    break
  fi
  
  # Display validation results
  echo "---------------------"
  echo "⚠️ VALIDATION ISSUES (Attempt $((ATTEMPT-1))):"
  echo "---------------------"
  echo "$VALIDATION_RESULT"
  echo "---------------------"
  
  # Create self-correction prompt
  CORRECTION_PROMPT="You are a solution improver.
Below is a solution and validation feedback identifying issues. 
Revise the solution to fix ALL identified issues while maintaining quality.

ORIGINAL SOLUTION:
$CURRENT_OUTPUT

VALIDATION ISSUES:
$VALIDATION_RESULT

TASK: $TASK

VALIDATION CRITERIA: $VALIDATION_CRITERIA

Return only the corrected solution without explaining your changes."

  echo "🔧 Self-correcting based on validation feedback (Attempt $ATTEMPT)..."
  CURRENT_OUTPUT=$(llm "$CORRECTION_PROMPT")
  
  # Display the corrected solution
  echo "---------------------"
  echo "📝 CORRECTED SOLUTION (Attempt $ATTEMPT):"
  echo "---------------------"
  echo "$CURRENT_OUTPUT"
  echo "---------------------"
done

########################################
# 3. FINAL RESULT AS JSON
########################################
# Create JSON output with the final solution
JSON_PROMPT="Convert the following Python solution into a valid JSON structure with the solution code as a string value.
Format it exactly as:
{
  \"solution\": \"<SOLUTION_CODE_HERE>\",
  \"iterations\": <NUMBER_OF_ITERATIONS>,
  \"task\": \"<TASK_DESCRIPTION>\"
}

Ensure proper escaping of any quotes or special characters in the code.

CODE:
$CURRENT_OUTPUT

TASK: $TASK
ITERATIONS: $ATTEMPT"

JSON_OUTPUT=$(llm "$JSON_PROMPT")

# Only output the JSON result
echo "$JSON_OUTPUT"

exit 0