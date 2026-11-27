
import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from litellm import acompletion
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv(Path(__file__).parent.parent / ".env")

MODEL = os.getenv(
    "LLM_MODEL",
    "gemini/gemini-3.5-flash-lite"
)


async def main():
    # Start the MCP server
    params = StdioServerParameters(
        command="python",
        args=["server.py"]
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:

            # Connect to the MCP server
            await session.initialize()

            # Discover all available MCP tools
            available_tools = (await session.list_tools()).tools

            print("Discovered MCP tools:")
            for tool in available_tools:
                print("-", tool.name)

            # Convert MCP tools into Gemini-compatible schemas
            schemas = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema
                    }
                }
                for tool in available_tools
            ]

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a pharmacy stock assistant. "
                        "Use the available MCP tools to answer questions. "
                        "Never invent stock information. "
                        "Use read tools to check inventory. "
                        "Use record_sale only when a sale is requested. "
                        "Never claim a sale succeeded unless the tool confirms it."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Please record a sale of 2 packs "
                        "of Amoxicillin 500mg."
                    )
                }
            ]

            # Allow Gemini to request tools
            for step in range(5):
                response = await acompletion(
                    model=MODEL,
                    messages=messages,
                    tools=schemas,
                    tool_choice="auto"
                )

                message = response.choices[0].message

                messages.append(
                    message.model_dump(exclude_none=True)
                )

                if not message.tool_calls:
                    print("\nGemini's answer:")
                    print(message.content)
                    break

                # Execute each requested MCP tool
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    arguments = json.loads(
                        tool_call.function.arguments
                    )

                    print(f"\nCalling MCP tool: {name}")
                    print("Arguments:", arguments)

                    # Human approval required before recording a sale
                    if name == "record_sale":
                        print("\nSALE CONFIRMATION REQUIRED")
                        print("Medicine:", arguments.get("item"))
                        print("Strength:", arguments.get("strength"))
                        print("Quantity:", arguments.get("quantity"))

                        approval = input(
                            "Do you approve this sale? (yes/no): "
                        )

                        if approval.strip().lower() not in ("yes", "y"):
                            result_content = {
                                "success": False,
                                "message": (
                                    "Sale cancelled. "
                                    "Human approval was not given."
                                )
                            }

                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": json.dumps(result_content)
                            })

                            print("Sale cancelled.")
                            continue

                    # Call the MCP server
                    result = await session.call_tool(
                        name,
                        arguments
                    )

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(
                            result.model_dump(),
                            default=str
                        )
                    })

            else:
                print("Maximum tool-call steps reached.")


if __name__ == "__main__":
    asyncio.run(main())
