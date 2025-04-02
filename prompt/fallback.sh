#!/bin/bash
#
# FALLBACK PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Trying a primary model/approach first
#  2) Validating the response against specific criteria
#  3) Falling back to alternative models if validation fails
#
# This pattern enables graceful degradation and increased reliability
# by providing multiple paths to success with different models.

########################################
# CONFIGURATION AND VALIDATION RULES
########################################
# The prompt to send to each model in the fallback chain

INPUT_PROMPT="Solve the following simple scheduling problem:

A tech company needs to schedule 4 employees (Alice, Bob, Carlos, and Diana) for a project across Monday through Friday. Each day requires exactly 2 employees to be working.

Given these constraints:
1. The schedule for Monday MUST be Carlos and Diana.
2. The schedule for Tuesday MUST be Alice and Carlos.
3. The schedule for Wednesday MUST be Bob and Diana.
4. The schedule for Thursday MUST be Alice and Diana.
5. The schedule for Friday MUST be Alice and Bob.

Provide ONLY a JSON response with the solution, following this exact format with no additional text:
{
  \"solution\": {
    \"Monday\": [\"Carlos\", \"Diana\"],
    \"Tuesday\": [\"Alice\", \"Carlos\"],
    \"Wednesday\": [\"Bob\", \"Diana\"],
    \"Thursday\": [\"Alice\", \"Diana\"],
    \"Friday\": [\"Alice\", \"Bob\"]
  }
}

Make sure your solution exactly matches the required schedule."
FINAL_OUTPUT_FILE="schedule.json"
JSON_FILE="schedule_temp.json"

# Validation function using jq
validate_response() {
  local result="$1"
  local model_name="$2"s

  # Try to extract JSON content
  echo "$result" > "$JSON_FILE"
  
  # First check: Is the JSON valid?
  if ! jq empty "$JSON_FILE" 2>/dev/null; then
    echo "Validation for $model_name: Invalid JSON"
    return 1
  fi
  
  echo "Validation for $model_name:"
  echo "- Valid JSON: true"
  
  # Second check: Does it have a solution object?
  if ! jq -e '.solution' "$JSON_FILE" > /dev/null 2>&1; then
    echo "- Missing solution object"
    return 1
  fi
  
  # Third check: Does it have all 5 days?
  for day in "Monday" "Tuesday" "Wednesday" "Thursday" "Friday"; do
    if ! jq -e ".solution.\"$day\"" "$JSON_FILE" > /dev/null 2>&1; then
      echo "- Missing day: $day"
      return 1
    fi
  done
  echo "- All days present: true"
  
  # Fourth check: Each day has exactly 2 employees
  local invalid_days=""
  for day in "Monday" "Tuesday" "Wednesday" "Thursday" "Friday"; do
    local count
    count=$(jq ".solution.\"$day\" | length" "$JSON_FILE")
    if [ "$count" != "2" ]; then
      invalid_days="$invalid_days $day"
    fi
  done
  
  if [ -n "$invalid_days" ]; then
    echo "- Days with wrong number of employees:$invalid_days"
    return 1
  else
    echo "- All days have exactly 2 employees"
  fi
  
  # Fifth check: Expected schedules for each day
  declare -A expected
  expected["Monday"]="Carlos Diana"
  expected["Tuesday"]="Alice Carlos"
  expected["Wednesday"]="Bob Diana"
  expected["Thursday"]="Alice Diana"
  expected["Friday"]="Alice Bob"
  
  local incorrect_days=""
  
  for day in "Monday" "Tuesday" "Wednesday" "Thursday" "Friday"; do
    # Get the scheduled employees for this day
    local employees
    employees=$(jq -r ".solution.\"$day\"[]" "$JSON_FILE" | sort | tr '\n' ' ' | sed 's/ $//')
    
    # Compare with expected
    if [ "$employees" != "${expected[$day]}" ]; then
      incorrect_days="$incorrect_days $day"
    fi
  done
  
  if [ -n "$incorrect_days" ]; then
    echo "- Days with incorrect employee assignments:$incorrect_days"
    return 1
  else
    echo "- All days have correct employee assignments"
  fi
  
  echo "✓ All constraints validated successfully"
  return 0  # Success
}

########################################
# FALLBACK CHAIN EXECUTION
# 
# Try models in sequence, falling back to the next one if validation fails
########################################
echo "---------------------"
echo "🔄 FALLBACK PROMPT PATTERN DEMO"
echo "---------------------"
echo "Task: Generate a valid employee schedule following constraints"
echo "Trying models in fallback sequence..."
echo "---------------------"

for model in "o1-mini" "4o-mini" "gpt4"; do
  echo "🚀 Attempt with model: $model..."
  
  # Call the model
  result=$(llm --model "$model" "$INPUT_PROMPT" 2>/dev/null)
  
  # Check if the model call was successful
  if [ $? -ne 0 ]; then
    echo "⚠️ Error calling $model. Check your connection or API access."
    continue
  fi
  
  # Validate the result
  if validate_response "$result" "$model"; then
    echo "✅ Validation passed with $model"
    
    # Save the result
    cat "$JSON_FILE" > "$FINAL_OUTPUT_FILE"
    
    # Print the solution in a readable format
    echo "---------------------"
    echo "📋 FINAL SOLUTION (using $model):"
    echo "---------------------"
    for day in Monday Tuesday Wednesday Thursday Friday; do
      employees=$(jq -r ".solution.\"$day\" | join(\", \")" "$FINAL_OUTPUT_FILE")
      echo "$day: $employees"
    done
    echo "---------------------"
    
    rm -f "$JSON_FILE"
    
    echo "✅ Fallback prompt pattern demonstration complete!"
    echo "This pattern increases reliability by providing multiple paths"
    echo "to task completion, falling back to different models when needed."
    exit 0
  else
    echo "⚠️ $model result didn't meet criteria. Falling back to next model."
    echo "---------------------"
  fi
done

echo "❌ All models in the fallback chain failed to produce a valid solution."
rm -f "$JSON_FILE"
exit 1