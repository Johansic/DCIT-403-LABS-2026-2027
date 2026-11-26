
import ast
import operator
import requests


def calculator(expression):
    """
    Safely evaluate basic arithmetic expressions.
    Supports addition, subtraction, multiplication and division.
    Does not use eval().
    """

    expression = expression.replace(",", "")

    operations = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }

    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in operations:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Div) and right == 0:
                raise ValueError("Cannot divide by zero")

            return operations[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in operations:
            return operations[type(node.op)](evaluate(node.operand))

        raise ValueError("Unsupported mathematical expression")

    try:
        tree = ast.parse(expression, mode="eval")
        return evaluate(tree.body)

    except Exception as error:
        return f"Error: {error}"


def wiki_lookup(title):
    """
    Search Wikipedia and return a short summary.
    """

    url = (
        "https://en.wikipedia.org/api/rest_v1/page/summary/"
        + requests.utils.quote(title.replace(" ", "_"))
    )

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "DCIT403-lab"},
            timeout=10
        )

        if response.status_code == 404:
            return "No Wikipedia article found for this topic."

        response.raise_for_status()
        data = response.json()

        return data.get("extract", "No summary available.")[:800]

    except requests.RequestException as error:
        return f"Wikipedia lookup failed: {error}"
