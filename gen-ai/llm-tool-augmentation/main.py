import json
from typing import Dict, Any

from huggingface_hub import InferenceClient

from config import MODEL_URL, SYSTEM_PROMPT_TEMPLATE
from tools import registry


class ChatBot:
    def __init__(self):
        self._client = InferenceClient(model=MODEL_URL)
        self._system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            tool_descriptions=registry.get_tool_descriptions()
        )

    def chat(self, user_prompt: str) -> Dict[str, Any]:
        """Send a chat message and return the parsed response."""
        try:
            response = self._client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"{self._system_prompt} {user_prompt}",
                    }
                ],
            )
            json_content = response.choices[0].message.content
            return json.loads(json_content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse response as JSON: {e}")
        except Exception as e:
            raise RuntimeError(f"Chat request failed: {e}")

    def execute_tool(self, response: Dict[str, Any]) -> None:
        """Safely execute a tool based on the response."""
        if not response.get("tool_use"):
            print("No tool execution requested.")
            return

        tool_name = response.get("tool_name")
        if not tool_name:
            raise ValueError("Tool name not specified in response")

        # Extract tool parameters (excluding metadata)
        tool_params = {k: v for k, v in response.items()
                       if k not in ["tool_use", "tool_name"]}

        try:
            registry.execute(tool_name, **tool_params)
        except Exception as e:
            print(f"Error executing tool '{tool_name}': {e}")


def main():
    """Main application entry point."""
    bot = ChatBot()

    try:
        prompt = input("How can I help you? ")
        response = bot.chat(prompt)
        bot.execute_tool(response)
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
