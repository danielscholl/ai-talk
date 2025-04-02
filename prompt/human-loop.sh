#!/usr/bin/env bash
#
# HUMAN-IN-THE-LOOP PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Using an initial prompt to generate content
#  2) Getting human feedback
#  3) Refining the output based on that feedback
#  4) Repeating until the human is satisfied
#
# This pattern integrates human expertise with AI generation for
# higher-quality, collaboratively refined outputs.

########################################
# TASK DEFINITION
########################################
# Single focused task for demonstration purposes
TASK="Create a marketing email for a new online course on AI basics"

echo "---------------------"
echo "🔄 HUMAN-IN-THE-LOOP PROMPT PATTERN DEMO"
echo "---------------------"
echo "Task to be completed:"
echo "$TASK"
echo "---------------------"

########################################
# 1. INITIAL GENERATION PHASE
# 
# Create the first version of content with an initial prompt
########################################
INITIAL_PROMPT="You are a marketing content creator.
Generate a marketing email for the following task:

TASK: $TASK

Create professional-quality content that is engaging and persuasive.
The email should have a clear subject line, compelling introduction,
key benefits, and a strong call to action."

echo "✍️ Phase 1: Generating initial content..."
CURRENT_OUTPUT=$(llm "$INITIAL_PROMPT")

# Display the initial output
echo "---------------------"
echo "📝 INITIAL OUTPUT (Iteration 1):"
echo "---------------------"
echo "$CURRENT_OUTPUT"
echo "---------------------"

########################################
# 2. FEEDBACK LOOP PHASE
# 
# Iteratively improve the content based on human feedback
########################################
ITERATION=1
FEEDBACK=""

while true; do
  echo "📋 Provide your feedback for improvement (or type 'done' to finish):"
  read FEEDBACK
  
  # Check if we're done with iterations
  if [ "$FEEDBACK" = "done" ]; then
    break
  fi
  
  # Increment iteration counter
  ITERATION=$((ITERATION + 1))
  
  # Create refinement prompt that includes previous output and feedback
  REFINEMENT_PROMPT="You are a content refinement specialist.
Below is a marketing email and human feedback on how to improve it.
Revise the email to incorporate the feedback while maintaining quality and persuasiveness.

ORIGINAL EMAIL:
$CURRENT_OUTPUT

HUMAN FEEDBACK:
$FEEDBACK

TASK: $TASK

Return only the revised email without explaining your changes."

  echo "🔄 Refining content based on your feedback (Iteration $ITERATION)..."
  CURRENT_OUTPUT=$(llm "$REFINEMENT_PROMPT")
  
  # Display the refined output
  echo "---------------------"
  echo "📝 REFINED OUTPUT (Iteration $ITERATION):"
  echo "---------------------"
  echo "$CURRENT_OUTPUT"
  echo "---------------------"
done

########################################
# 3. FINAL RESULT
########################################
echo "---------------------"
echo "✅ FINAL RESULT (after $ITERATION iterations):"
echo "---------------------"
echo "$CURRENT_OUTPUT"
echo "---------------------"

echo "✅ Human-in-the-Loop prompt pattern demonstration complete!"
echo "This pattern combines the efficiency of AI with human expertise,"
echo "resulting in higher quality outputs that better align with"
echo "specific needs and requirements."
exit 0