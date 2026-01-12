"""Tool definitions and registry for the chatbot."""

from typing import Dict, Callable, Any


class ToolRegistry:
    """Registry for managing available tools."""
    
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
    
    def register(self, name: str, description: str, func: Callable):
        """Register a tool with its metadata."""
        self._tools[name] = {
            'description': description,
            'function': func
        }
    
    def get_tool_descriptions(self) -> str:
        """Get formatted descriptions of all registered tools."""
        return "\n-------\n".join([
            f"Name: {name}\n\n{tool['description']}"
            for name, tool in self._tools.items()
        ])
    
    def execute(self, tool_name: str, **kwargs) -> Any:
        """Safely execute a tool by name."""
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name]['function'](**kwargs)


# Tool registry instance
registry = ToolRegistry()


def current_weather(location: str) -> None:
    """Get current weather for a location."""
    print(f"The current weather in {location} is 21 degree celsius.")


# Register tools
registry.register(
    "current_weather",
    """Description: Use this tool to find the current weather of a given location. If you need the current weather of a 
location in the world, this is the tool to use. This tool gives you the accurate current weather at any given point 
in time for a given location on the world. 
Input: (location)

Example user prompts and expected responses: 

User: What is the current weather in Chennai, India? 
Response: {"tool_use": true, "tool_name": "current_weather", "location": "Chennai, Tamil Nadu, India"}

User: What is the weather in San Jose? 
Response: {"tool_use": true, "tool_name": "current_weather", "location": "San Jose, CA, USA"}

User: Latest weather in Montreal? 
Response: {"tool_use": true, "tool_name": "current_weather", "location": "Montreal, Canada"}""",
    current_weather
)