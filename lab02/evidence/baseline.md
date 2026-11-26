
# Lab 2 – Baseline Experiment

## Objective
To evaluate the Gemini language model's ability to perform calculations and answer factual questions without using external tools.

## Model
gemini/gemini-3.5-flash-lite

## Part A: Budget Questions

Question used for all three tests:

"I have GHS 1,200. I want 4 bags of rice at GHS 185 each and 3 gallons of oil at GHS 95 each. How much will I have left?"

Correct calculation:
- Rice: 4 × 185 = GHS 740
- Oil: 3 × 95 = GHS 285
- Total cost: GHS 1,025
- Remaining balance: GHS 175

| Test | Model's Answer | Correct? |
|---|---|---|
| Budget Test 1 | GHS 175 | Yes |
| Budget Test 2 | GHS 175 | Yes |
| Budget Test 3 | GHS 175 | Yes |

Observation: The model correctly calculated the remaining balance in all three attempts. The wording varied slightly, but the final answer remained consistent.

## Part B: Factual Questions

| Test | Question | Model's Answer | Correct? |
|---|---|---|---|
| Fact Test 1 | What is the capital of the Bono East Region of Ghana? | Techiman | Yes |
| Fact Test 2 | What is the capital city of Ghana? | Accra | Yes |

Confidence observation: The model presented both answers directly and confidently without expressing uncertainty.

## Conclusion

The model successfully answered all five questions without using tools. It correctly performed the budget calculations and answered both factual questions.

However, relying entirely on the language model for calculations may be unreliable in more complex situations. This motivates the use of external tools, such as a calculator, in a ReAct agent.
