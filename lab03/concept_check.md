
# Lab 3: Percepts and Actions as Tools: Function Calling and MCP: Concept Check

## Q1. List one advantage and one disadvantage of native function calling compared with the Lab 2 text protocol.

**Answer:**

One advantage of native function calling is that the model produces structured tool calls with clearly defined function names and arguments. This makes it easier for the application to identify and execute the correct function without manually interpreting text such as `Action:` and `Action Input:`.

One disadvantage is that native function calling depends on the model provider supporting the feature and its specific tool-calling format.

## Q2. In MCP, what is the difference between a tool and a resource? Give a pharmacy example of each.

**Answer:**

An MCP tool is a function that an AI assistant can call to perform an operation, while a resource provides data or information that the assistant can access as context.

For example, `check_stock` is a tool because it performs a search for a particular medicine in the pharmacy inventory. The pharmacy stock CSV file can serve as a resource because it contains inventory information that the assistant can access.

## Q3. Why should `record_sale` check the quantity even though the system prompt already says "never oversell"?

**Answer:**

The system prompt gives the AI assistant instructions, but it does not guarantee that the assistant will always make the correct decision. The model could misunderstand a request or provide an incorrect quantity.

Therefore, `record_sale` must enforce its own safety checks before changing the stock. It should reject quantities that are zero or negative and prevent a sale when the requested quantity exceeds the available stock. This ensures that the pharmacy inventory remains accurate even if the AI makes a mistake.

## Q4. Which messages in the worked example are percepts?

**Answer:**

Message 3 is the percept because it contains the result returned by the `check_stock` tool. It provides information about the medicine, its strength and the available quantity.

Message 2 is the assistant's decision to call the tool, while message 4 is the assistant's final response to the user. Therefore, message 3 is the percept.
