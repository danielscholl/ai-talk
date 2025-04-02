#!/bin/bash
#
# SNOWBALL PROMPT CHAIN EXAMPLE (Bash)
#
# This script demonstrates the pattern of:
#  1) Starting with a small, simple prompt
#  2) Using each output as input to the next, more complex prompt
#  3) Gradually building up to the final complex output
#
# This pattern enables progressive refinement and expansion,
# similar to how a snowball grows as it rolls downhill.

########################################
# TOPIC DEFINITION
########################################
# The core topic that starts the snowball chain
TOPIC="The Impact of AI on Software Development"

echo "---------------------"
echo "🔄 SNOWBALL PROMPT PATTERN DEMO"
echo "---------------------"
echo "Starting topic:"
echo "$TOPIC"
echo "---------------------"

########################################
# 1. INITIAL SMALL PROMPT
# 
# Start with a simple task (generating a title)
########################################
echo "Step 1: Generate Title"
TITLE=$(llm "Create a catchy title for a blog post on: $TOPIC")
echo "Title: $TITLE"
echo "---------------------"

########################################
# 2. FIRST EXPANSION
# 
# Use the title to generate a structured outline
########################################
echo "Step 2: Generate Outline"
OUTLINE=$(llm "Generate a blog post outline for: $TITLE")
echo "Outline:"
echo "$OUTLINE"
echo "---------------------"

########################################
# 3. SECOND EXPANSION
# 
# Use the outline to create a full draft
########################################
echo "Step 3: Expand Outline into Full Draft"
DRAFT=$(llm "Write a full blog post based on this outline:\n$OUTLINE")
echo "Draft generated (length: $(echo "$DRAFT" | wc -w) words)"
echo "---------------------"

########################################
# 4. FINAL REFINEMENT
# 
# Format the draft into the final polished output
########################################
echo "Step 4: Final Output"
HTML=$(llm "Convert this blog post into a nice html page:\n$DRAFT")
echo "Final Output:"
echo "$HTML"
echo "---------------------"

echo "✅ Snowball prompt pattern demonstration complete!"
echo "This pattern enables progressive refinement and expansion,"
echo "building complex outputs through a series of increasingly detailed prompts."
exit 0
