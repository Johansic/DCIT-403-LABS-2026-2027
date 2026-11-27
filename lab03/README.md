
# Lab 3: Percepts and Actions as Tools — Function Calling and MCP

## 1. Overview

This laboratory demonstrates how an intelligent agent interacts with its environment using native function calling and the Model Context Protocol (MCP).

The project implements a pharmacy stock assistant that can check medicine availability, search inventory, identify medicines approaching their expiry dates and record sales.

## 2. Learning Objectives

- Understand native function calling compared with the Lab 2 text-based tool protocol.
- Understand MCP hosts, clients, servers and tools.
- Build an MCP server using FastMCP.
- Connect an AI agent to MCP tools using Gemini.
- Distinguish between percepts (read operations) and actions (write operations).
- Apply validation and human approval before changing pharmacy stock.

## 3. Project Structure

```text
lab03/
├── README.md
├── concept_check.md
├── function_calling.py
├── server.py
├── client_agent.py
├── data/
│   ├── pharmacy_stock.csv
│   └── pharmacy_stock_backup.csv
└── evidence/
    └── tool_calls.jsonl
```

## 4. Technologies Used

- Python 3.11
- LiteLLM
- Google Gemini
- Model Context Protocol (MCP)
- FastMCP
- MCP Inspector
- CSV for pharmacy inventory storage

## 5. Native Function Calling

The `function_calling.py` program defines a `check_stock` function and exposes it to Gemini using a structured JSON tool schema.

Gemini can request the function, and Python executes it and returns the result to the model.

This replaces the manual text parsing used in the Lab 2 ReAct protocol.

## 6. MCP Server Tools

The `server.py` program exposes four tools:

| Tool | Description | Classification |
|---|---|---|
| check_stock | Checks stock by medicine and strength | Read / Percept |
| search_items | Searches inventory by name, strength or form | Read / Percept |
| list_expiring | Lists medicines expiring within a specified number of days | Read / Percept |
| record_sale | Records a sale and reduces available stock | Write / Action |

## 7. MCP Client Agent

The `client_agent.py` program:

1. Starts the MCP server as a subprocess.
2. Establishes a connection using stdio.
3. Discovers available tools through `session.list_tools()`.
4. Converts the discovered tools into Gemini-compatible schemas.
5. Sends user requests to Gemini.
6. Executes requested MCP tools.
7. Returns tool results to Gemini for its final response.

Human approval is required before the `record_sale` tool can execute.

## 8. Safety and Validation

The `record_sale` tool includes three important checks:

- The quantity must be greater than zero.
- The medicine and strength must exist in the inventory.
- The requested quantity must not exceed available stock.

The client also requires human approval before recording a sale.

These controls help prevent incorrect stock updates.

## 9. Testing and Results

The following tests were performed:

| Test | Expected result | Actual result |
|---|---|---|
| Negative sale quantity (-5) | Reject sale | Passed |
| Sell 50 packs when 40 were available | Reject sale | Passed |
| Sell 5 packs | Accept sale; 35 remaining | Passed |
| Gemini requests sale of 2 packs | Require approval; 33 remaining | Passed |
| MCP tool discovery | Discover four tools | Passed |

The final live stock quantity for Amoxicillin 500mg was 33 packs.

The backup file preserved the original quantity of 40 packs.

## 10. Evidence

The `evidence/` directory contains:

- `tool_calls.jsonl`: Records the tested sale operations and their results.

Additional screenshots of MCP Inspector and the Gemini client execution should be captured and stored in this directory.

## 11. Conclusion

This laboratory demonstrated how an intelligent agent can use native function calling and MCP to interact with external tools.

Read tools provide percepts that help the agent understand its environment, while write tools perform actions that change the environment.

The pharmacy assistant demonstrated this distinction by retrieving inventory information and recording sales. Validation checks and human approval were used to make write operations safer and more reliable.
```

