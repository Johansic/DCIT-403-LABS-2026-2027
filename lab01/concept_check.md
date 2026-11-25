# Lab 1: Agents Then and Now: PEAS and Your First LLM Call: Concept Check

Answer in your own words before the Wednesday session (independent work). Your answers feed Section 2 of your lab report (Concept and classical root).

## Q1. Give the PEAS description of a self-checkout machine at a supermarket.

_Your answer:_
PEAS component	Description
Performance Measure	Accurate scanning, correct payment processing, reduced waiting time, and customer satisfaction.
Environment	Supermarket, customers, products, barcodes, shopping baskets, and payment systems.
Actuators	Display screen, speakers, receipt printer, payment terminal, and checkout gate.
Sensors	Barcode scanner, weighing scale, touchscreen, and card reader.

Explanation: The machine uses sensors to receive information, processes the customer's shopping activities, and uses actuators to respond. Its performance is measured by how accurately and efficiently it completes checkout.

## Q2. Is the Campus Info Bot's environment episodic or sequential? Justify your answer using what the bot needs to remember.

_Your answer:_ Sequential
The Campus Info Bot operates in a sequential environment because its current responses can depend on previous messages in the conversation. It needs to remember the conversation history so that it can understand follow-up questions and provide relevant answers.

Explanation: Imagine this conversation:
- Student: Where is the Computer Science Department office?
- Bot: It is in the Department of Computer Science building.
- Student: What time does it close?
The bot needs to remember the previous question to understand what "it" refers to.


## Q3. Which part of an LLM agent plays the role of the percept sequence?

_Your answer:_The conversation history, stored in the messages list, plays the role of the percept sequence. It contains the previous inputs and interactions that the LLM uses to understand the current situation and generate an appropriate response.

Explanation: In our campus_bot.py, we used:
messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]


Each new user question and bot response is added to this list. The accumulated messages provide the context for the next response.


## Q4. An agent gives a wrong office location because its facts block was out of date. Was it irrational? Explain.

_Your answer:_Not necessarily. The agent may have acted rationally based on the information available in its facts block at the time. However, the information was outdated, which caused it to give an incorrect answer. To improve its performance, the facts block should be regularly updated so that the agent can provide accurate information.

Explanation: Rationality is judged based on the information available to the agent and how well its actions achieve its performance measure. An agent cannot reliably provide information it does not have.

