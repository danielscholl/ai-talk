#!/usr/bin/env bash
#
# DECISION MAKER PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Using a "decision prompt" to classify input
#  2) Parsing the classification result
#  3) Running different prompt chains based on the classification
#
# This is a simplified educational example focusing on the decision maker pattern.

########################################
# CONFIGURABLE INPUT SELECTION
########################################
# Get example number from command line argument, default to 1 if not provided
EXAMPLE_NUMBER=${1:-1}

# Define different example inputs
case "$EXAMPLE_NUMBER" in
  1)
    SAMPLE_INPUT="I need help understanding how to diversify my investment portfolio"
    echo "Example 1: Financial question selected"
    ;;
  2)
    SAMPLE_INPUT="How do I set up a secure home network with proper Wi-Fi encryption?"
    echo "Example 2: Technical question selected"
    ;;
  3)
    SAMPLE_INPUT="Can you explain the benefits of regular exercise for mental health?"
    echo "Example 3: General health question selected"
    ;;
  *)
    SAMPLE_INPUT="I need help understanding how to diversify my investment portfolio"
    echo "Invalid example number '$EXAMPLE_NUMBER', defaulting to Example 1"
    ;;
esac

echo "---------------------"
echo "🔍 DECISION MAKER PROMPT PATTERN DEMO"
echo "---------------------"
echo "Input to be classified:"
echo "$SAMPLE_INPUT"
echo "---------------------"

########################################
# 2. DECISION PROMPT
# 
# The decision prompt analyzes the input and determines which path to take
########################################
DECISION_PROMPT="You are a content classifier.
Analyze the following request and classify it into exactly ONE category:
FINANCIAL, TECHNICAL, or GENERAL.
Return only the category name without explanation or additional text.

REQUEST: $SAMPLE_INPUT"

echo "🧠 Running decision prompt to classify the input..."
# Call the LLM to get a real classification
DECISION_OUTPUT=$(llm "$DECISION_PROMPT")

echo "Decision: $DECISION_OUTPUT"
echo "---------------------"

########################################
# 3. SPECIALIZED PROMPT CHAINS
# 
# Each chain represents a different processing path optimized for that category
########################################

run_financial_chain() {
  echo "💰 Running FINANCIAL specialized chain..."
  
  FINANCIAL_PROMPT="You are a financial advisor assistant.
Provide helpful guidance on the following financial question:
$SAMPLE_INPUT

Keep your response focused on educational financial information."

  # Call the LLM with the financial prompt
  RESPONSE=$(llm "$FINANCIAL_PROMPT")
  echo "$RESPONSE"
}

run_technical_chain() {
  echo "🔧 Running TECHNICAL specialized chain..."
  
  TECHNICAL_PROMPT="You are a technical support assistant.
Provide clear technical guidance on the following question:
$SAMPLE_INPUT

Focus on practical steps and technical accuracy."

  # Call the LLM with the technical prompt
  RESPONSE=$(llm "$TECHNICAL_PROMPT")
  echo "$RESPONSE"
}

run_general_chain() {
  echo "📚 Running GENERAL information chain..."
  
  GENERAL_PROMPT="You are a helpful assistant.
Provide general information on the following question:
$SAMPLE_INPUT

Be informative but concise."

  # Call the LLM with the general prompt
  RESPONSE=$(llm "$GENERAL_PROMPT")
  echo "$RESPONSE"
}

########################################
# 4. EXECUTE THE APPROPRIATE CHAIN
# 
# Route to the specialized chain based on the decision prompt's output
########################################
case "$DECISION_OUTPUT" in
  "FINANCIAL")
    run_financial_chain
    ;;
  "TECHNICAL")
    run_technical_chain
    ;;
  "GENERAL")
    run_general_chain
    ;;
  *)
    echo "⚠️ Unrecognized category. Defaulting to GENERAL chain..."
    run_general_chain
    ;;
esac

echo "---------------------"
echo "✅ Decision maker prompt pattern demonstration complete!"
echo "This pattern enables intelligent branching in prompt chains"
echo "for more responsive and context-aware AI applications."
exit 0
