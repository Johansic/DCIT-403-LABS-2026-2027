
import os
from dotenv import load_dotenv
from litellm import completion

# Load environment variables
load_dotenv()
MODEL = os.getenv("LLM_MODEL")

# University information available to the bot
FACTS = """
1. The Computer Science Department office is located in the
   Department of Computer Science building.
2. The department office opens from Monday to Friday,
   8:00 AM to 5:00 PM.
3. Students can visit the department office for academic enquiries.
4. The Department of Information Technology office handles
   enquiries related to Information Technology programmes.
5. Students should contact their department office for
   programme-specific academic assistance.
6. The bot cannot register students for courses or change grades.
"""

# Instructions that control the bot's behaviour
SYSTEM_PROMPT = f"""
You are the University of Ghana Campus Information Bot.

Your job is to help new students with basic university information.

Use ONLY the following facts to answer questions:
{FACTS}

Rules:
- Give clear and helpful answers.
- Do not invent information.
- If the information is not available in the facts, say:
  "I don't have that information. Please contact the relevant
  department office."
- You can provide information, but you cannot register students,
  book appointments, or change grades.
"""

# Store conversation history
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

print("Welcome to the University of Ghana Campus Info Bot!")
print("Ask me a question, or type 'quit' to exit.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower().strip() == "quit":
        print("Bot: Goodbye!")
        break

    # Add the student's question to conversation history
    messages.append({"role": "user", "content": user_input})

    try:
        response = completion(
            model=MODEL,
            messages=messages
        )

        bot_reply = response.choices[0].message.content

        # Add the bot's answer to conversation history
        messages.append({"role": "assistant", "content": bot_reply})

        print(f"Bot: {bot_reply}")

    except Exception as e:
        print("An error occurred:", e)
