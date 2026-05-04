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


def calculator(expression: str) -> str:
    """
    Safely evaluate a math expression.
    
    Args:
        expression: Math expression like "25 * 4" or "(10 + 5) / 3"
    
    Returns:
        Result as string or error message.
    """
    try:
        # Sirf safe characters allow karo
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.\%]+$', expression):
            return "Invalid expression. Only numbers and +,-,*,/,%,(,) allowed."
        
        # eval safe banaya - sirf math chal sakta hai (no imports, no functions)
        result = eval(expression, {"__builtins__": {}}, {})
        
        return f"Result: {result}"
    
    except ZeroDivisionError:
        return "Error: Division by zero"
    except SyntaxError:
        return "Error: Invalid math syntax"
    except Exception as e:
        return f"Calculator error: {str(e)}"