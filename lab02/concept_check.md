
# Lab 2 – Concept Check
## Architectures: A ReAct Agent From Scratch

### Question 1: Classify the following systems as reactive, deliberative or hybrid. Explain your answers.

**a. Thermostat – Reactive Architecture**

A thermostat is a reactive agent because it responds directly to changes in temperature using predefined condition-action rules. For example, when the temperature falls below a specified level, it switches on the heater. It does not need to develop a complex plan before acting.

**b. Chess Engine – Deliberative Architecture**

A chess engine is primarily deliberative because it evaluates possible moves, considers future game states and selects a move based on strategic reasoning. It searches through possible outcomes before deciding what action to take.

**c. ReAct Agent – Hybrid Architecture**

A ReAct agent is hybrid because it combines deliberative reasoning with reactive actions. It reasons about what needs to be done, selects an appropriate tool, executes the action and observes the result before deciding what to do next.

### Question 2: In the budget calculation trace, which lines are percepts and which are actions?

**Actions:**
- Action: calculator
- Action Input: 4*185 + 3*95
- Action: calculator
- Action Input: 1200 - 1025
- Action: finish
- Action Input: You will have GHS 175 left.

These lines represent actions because they describe the operations selected and executed by the agent.

**Percepts:**
- The original budget question.
- Observation: 1025
- Observation: 175

These are percepts because they provide information received by the agent from its environment or tools.

The Thought lines represent the agent's internal reasoning rather than external percepts or actions.

### Question 3: Why do we pass stop=["Observation:"] when calling the model?

We pass stop=["Observation:"] to prevent the language model from generating its own observation or pretending that a tool has already been executed.

The Python program should execute the selected tool and return the actual result as an observation.

This makes the ReAct process more reliable because the agent receives genuine results from the tools instead of invented information.

### Question 4: Map the budget calculation trace to BDI terms.

**Belief:**

The agent's beliefs include the information provided in the original question and the observations received from the calculator.

For example, the agent knows the initial budget is GHS 1,200 and receives the observation that the total cost is GHS 1,025.

**Desire:**

The agent's desire is to determine how much money will remain after purchasing the rice and oil.

**Intention:**

The agent's intention is its chosen plan to achieve the goal. It decides to use the calculator to determine the total cost and then subtract that amount from the initial budget.

The agent executes this plan through calculator actions and eventually selects the finish action.

### Conclusion

The ReAct architecture combines reasoning, tool execution and observation. It demonstrates how an intelligent agent can use its beliefs, goals and intentions to solve problems through interaction with its environment.
