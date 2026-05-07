"""
Calculator Tool - Safe math expression evaluator.
NEVER use eval() in production - security risk!
"""
import re
import operator


# Allowed operators
OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '%': operator.mod,
    '**': operator.pow,
}

# Matches percentage expressions:
#   "20% of 500"   → 100.0
#   "500 + 20%"    → 600.0  (add 20% of 500)
#   "500 - 20%"    → 400.0  (subtract 20% of 500)
#   "20%"          → 0.2
_PCT_OF   = re.compile(r'^([\d.]+)%\s+of\s+([\d.]+)$', re.IGNORECASE)
_PCT_OP   = re.compile(r'^([\d.]+)\s*([+\-])\s*([\d.]+)%$')
_PCT_BARE = re.compile(r'^([\d.]+)%$')


def _try_percentage(expression: str):
    """Return result string if expression is a percentage pattern, else None."""
    expr = expression.strip()

    m = _PCT_OF.match(expr)
    if m:
        pct, base = float(m.group(1)), float(m.group(2))
        return f"Result: {pct / 100 * base}"

    m = _PCT_OP.match(expr)
    if m:
        base, op, pct = float(m.group(1)), m.group(2), float(m.group(3))
        delta = pct / 100 * base
        result = base + delta if op == '+' else base - delta
        return f"Result: {result}"

    m = _PCT_BARE.match(expr)
    if m:
        return f"Result: {float(m.group(1)) / 100}"

    return None


def calculator(expression: str) -> str:
    """
    Safely evaluate a math expression.

    Supports standard arithmetic and percentage expressions:
        "25 * 4"        → Result: 100
        "20% of 500"    → Result: 100.0
        "500 + 20%"     → Result: 600.0
        "500 - 15%"     → Result: 425.0
        "20%"           → Result: 0.2

    Args:
        expression: Math expression string.

    Returns:
        Result as string or error message.
    """
    if not expression or not expression.strip():
        return "Invalid expression. Only numbers and +,-,*,/,%,(,) allowed."

    pct_result = _try_percentage(expression)
    if pct_result:
        return pct_result

    try:
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.\%]+$', expression):
            return "Invalid expression. Only numbers and +,-,*,/,%,(,) allowed."

        result = eval(expression, {"__builtins__": {}}, {})
        return f"Result: {result}"

    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid math syntax"
    except Exception as e:
        return f"Calculator error: {str(e)}"