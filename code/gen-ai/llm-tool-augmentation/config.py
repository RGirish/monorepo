"""Configuration settings for the chatbot."""

# API Configuration
MODEL_URL = "http://localhost:1234"

# System prompt template
SYSTEM_PROMPT_TEMPLATE = """
Below, you are given a user prompt along with a set of tools that you are able to use. To answer a given user prompt, 
you can choose to respond by selecting a tool to run. To know which tool to use for which scenario, you can read the 
description field of the tool. You can select a tool to use by responding in the specified JSON format, by providing 
the name of the tool along with the input to the tool. 

The tools available to you are: 

{tool_descriptions}

With the information above, answer the following user prompt: 

"""