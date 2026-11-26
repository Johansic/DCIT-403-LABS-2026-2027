
import os
import re
import time

from dotenv import load_dotenv
from litellm import completion

from lab02.tools import calculator, wiki_lookup

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "gemini/gemini-3.5-flash-lite")


SYSTEM_PROMPT = """
You are a helpful ReAct intelligent agent.

You MUST respond using this format:

Thought: <brief explanation>
Action: calculator
Action Input: <mathematical expression>

OR

Thought: <brief explanation>
Action: wiki_lookup
Action Input: <Wikipedia topic>

OR

Thought: <brief explanation>
Action: finish
Action Input: <final answer>

Rules:
1. Use calculator for mathematical calculations.
2. Use wiki_lookup for factual information.
3. Use finish when you have enough information to answer.
4. Never invent observations or tool results.
5. Only use the three actions listed above.
6. Always include a space between Action and Input.
7. Keep your thoughts brief.
"""


ACTION_RE = re.compile(
    r"(?:Thought:\s*(.*?)\s*\n)?"
    r"Action:\s*(\w+)\s*\n"
    r"Action\s*Input:\s*(.*)",
    re.DOTALL | re.IGNORECASE
)


def parse_action(response_text):
    """Extract the thought, action and action input."""

    match = ACTION_RE.search(response_text)

    if not match:
        return None, None, None

    thought = (match.group(1) or "").strip()
    action = match.group(2).strip().lower()
    action_input = match.group(3).strip()

    return thought, action, action_input


def execute_action(action, action_input):
    """Execute the selected tool and return its result."""

    if action == "calculator":
        return calculator(action_input)

    elif action == "wiki_lookup":
        return wiki_lookup(action_input)

    elif action == "finish":
        return action_input

    else:
        return f"Error: Unknown action '{action}'"


def run_agent(question, max_steps=6):
    """Run the ReAct reasoning and tool-use loop."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question}
    ]

    print("\n" + "=" * 60)
    print("QUESTION:", question)
    print("=" * 60)

    for step in range(max_steps):

        print(f"\n--- Step {step + 1} ---")

        try:
            response = completion(
                model=MODEL,
                messages=messages,
                stop=["Observation:"]
            )

            model_output = response.choices[0].message.content or ""

        except Exception as error:
            error_message = str(error)

            if "503" in error_message or "high demand" in error_message.lower():
                print("Gemini is temporarily busy. Please try again shortly.")
            else:
                print("Model error:", error)

            return None

        print(model_output)

        thought, action, action_input = parse_action(model_output)

        if action is None:
            observation = (
                "Invalid response format. You must use:\n"
                "Thought: <brief explanation>\n"
                "Action: calculator, wiki_lookup, or finish\n"
                "Action Input: <input>"
            )

        elif action not in ("calculator", "wiki_lookup", "finish"):
            observation = f"Unknown action: {action}. Choose a valid action."

        elif action == "finish":
            print("\nFINAL ANSWER:")
            print(action_input)
            return action_input

        else:
            result = execute_action(action, action_input)
            observation = str(result)

        print("Observation:", observation)

        messages.append({
            "role": "assistant",
            "content": model_output
        })

        messages.append({
            "role": "user",
            "content": (
                f"Observation: {observation}\n"
                "Continue using the required format. "
                "If you have the answer, use the finish action."
            )
        })

    print("\nStopped: Maximum number of steps reached.")
    return "Maximum steps reached."


if __name__ == "__main__":

    print("DCIT 403 - ReAct Intelligent Agent")
    print("Type 'quit' to exit.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "quit":
            print("Goodbye!")
            break

        if not question:
            continue

        run_agent(question)
