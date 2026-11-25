
# PEAS Description – Campus Info Bot

## PEAS Table

| Component | Description |
|---|---|
| Performance Measure | Provides accurate, relevant, and helpful answers to students. Admits when it does not know an answer. |
| Environment | University of Ghana students, departmental offices, office locations, opening hours, and contact information. |
| Actuators | Displays text responses to students through the terminal. |
| Sensors | Receives and reads questions typed by students through the terminal. |

## Task Environment Classification

1. **Partially Observable:** The bot has access only to the information supplied to it and cannot observe the entire university environment.

2. **Stochastic:** Student questions and language-model responses may vary, so the outcome is not always predictable.

3. **Sequential:** Previous messages in a conversation can influence the bot's current response.

4. **Dynamic:** University office information, including opening hours and contact details, may change over time.

5. **Discrete:** The bot receives text inputs and produces text outputs.

6. **Multi-agent:** The environment involves the bot, students, and university staff who provide or update information.
