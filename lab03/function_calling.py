import json
import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from litellm import completion

load_dotenv(".env")

MODEL = os.getenv("LLM_MODEL", "gemini/gemini-3.5-flash-lite")
DATA = Path(__file__).parent / "data" / "pharmacy_stock.csv"


def check_stock(item, strength=""):
    """Find a medicine by name and optional strength."""

    with open(DATA, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    return [
        row for row in rows
        if item.lower() in row["item"].lower()
        and strength.lower() in row["strength"].lower()
    ]


tools = [
    {
        "type": "function",
        "function": {
            "name": "check_stock",
            "description": "Check pharmacy stock for a medicine by name and strength.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Name of the medicine"
                    },
                    "strength": {
                        "type": "string",
                        "description": "Medicine strength, for example 500mg"
                    }
                },
                "required": ["item", "strength"]
            }
        }
    }
]


def ask_pharmacy(question):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a pharmacy stock assistant. "
                "Use check_stock to answer stock questions. "
                "Do not invent stock information."
            )
        },
        {"role": "user", "content": question}
    ]

    response = completion(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message
    messages.append(message.model_dump(exclude_none=True))

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.function.name == "check_stock":
            arguments = json.loads(tool_call.function.arguments)
            result = check_stock(**arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

    final_response = completion(
        model=MODEL,
        messages=messages
    )

    return final_response.choices[0].message.content


if __name__ == "__main__":
    question = "Do we have Amoxicillin 500mg in stock?"
    print("Question:", question)
    print("Answer:", ask_pharmacy(question))