import re

# Define the Lambda calculus data structures
class Var:
    """Represents a variable."""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name

class Lambda:
    """Represents a lambda abstraction (λx. body)."""
    def __init__(self, param, body):
        self.param = param  # This is a Var
        self.body = body    # This is another lambda expression

    def __repr__(self):
        return f"(λ{self.param}. {self.body})"

    def __eq__(self, other):
        return isinstance(other, Lambda) and self.param == other.param and self.body == other.body

class App:
    """Represents a function application (f x)."""
    def __init__(self, func, arg):
        self.func = func  # Function to be applied
        self.arg = arg    # Argument to apply

    def __repr__(self):
        return f"({self.func} {self.arg})"

    def __eq__(self, other):
        return isinstance(other, App) and self.func == other.func and self.arg == other.arg

# Substitution function for beta-reduction
def substitute(expr, var, value):
    """Substitutes the variable `var` with the expression `value` in `expr`."""
    if isinstance(expr, Var):
        if expr.name == var.name:
            return value  # Substitute variable with its value
        else:
            return expr   # Variable does not match, return unchanged
    elif isinstance(expr, Lambda):
        if expr.param.name == var.name:
            return expr  # If variable is bound in this abstraction, don't substitute
        else:
            # Perform substitution in the body
            return Lambda(expr.param, substitute(expr.body, var, value))
    elif isinstance(expr, App):
        # Perform substitution in both the function and argument
        return App(substitute(expr.func, var, value), substitute(expr.arg, var, value))
    return expr

# Beta-reduction: Apply function to argument (function application)
def beta_reduce(expr):
    """Performs a single beta-reduction step if possible."""
    if isinstance(expr, App):
        if isinstance(expr.func, Lambda):
            # Beta-reduction step: substitute the argument into the function body
            return substitute(expr.func.body, expr.func.param, expr.arg)
        else:
            # Recursively reduce function and argument
            reduced_func = beta_reduce(expr.func)
            reduced_arg = beta_reduce(expr.arg)
            return App(reduced_func, reduced_arg)
    elif isinstance(expr, Lambda):
        # Recursively reduce the body of the lambda
        return Lambda(expr.param, beta_reduce(expr.body))
    else:
        return expr  # For variables, return unchanged

# Interpreter function without step counting
def interpret(expr):
    """Interprets (reduces) a lambda expression until it cannot be reduced further."""
    prev_expr = None
    while expr != prev_expr:  # Keep reducing until no change
        prev_expr = expr
        expr = beta_reduce(expr)
    return expr

# Parsing Functionality

def tokenize(expression):
    """Tokenizes the input string into meaningful parts with position tracking."""
    tokens = []
    position = 0

    # Add '.' to the tokenizing regex
    for match in re.finditer(r'λ|[().]|[^\s()λ.]+', expression):
        token = match.group(0)
        start_pos = match.start()
        end_pos = match.end()
        tokens.append((token, start_pos, end_pos))
        position = end_pos

    return tokens

def parse(tokens):
    """Parses tokens into a lambda expression."""
    if not tokens:
        raise SyntaxError("Empty expression")
    
    def parse_single(tokens):
        token, start_pos, end_pos = tokens.pop(0)

        if token == 'λ':  # Lambda abstraction
            if not tokens:
                raise SyntaxError(f"Expected parameter after 'λ' at position {start_pos}")
            param, param_start, param_end = tokens.pop(0)  # The parameter
            if not tokens or tokens[0][0] != '.':
                raise SyntaxError(f"Expected '.' after lambda parameter '{param}' at position {param_end}")
            tokens.pop(0)  # Remove the dot
            body = parse(tokens)  # Parse the body
            return Lambda(Var(param), body)
        elif token == '(':  # Start of an application or nested expression
            expr = parse(tokens)  # Parse the first part
            if not tokens or tokens[0][0] != ')':
                raise SyntaxError(f"Expected ')' at position {start_pos}")
            tokens.pop(0)  # Remove closing parenthesis
            return expr
        else:  # It's a variable
            return Var(token)  # Return variable

    # Parse a single expression (either a variable, lambda, or nested expression)
    expr = parse_single(tokens)

    # Handle function application (left-associative)
    while tokens and tokens[0][0] not in [')', '.']:  # While tokens left and not a closing parenthesis or dot
        next_expr = parse_single(tokens)
        expr = App(expr, next_expr)

    return expr

def parse_expression(expression):
    """Parses a string expression into a Lambda Calculus expression."""
    tokens = tokenize(expression)
    return parse(tokens)

# REPL Function
def repl():
    """Run a simple REPL for Lambda Calculus expressions."""
    print("Welcome to the Lambda Calculus REPL! Type 'exit' to quit.")
    while True:
        try:
            expr_input = input("λ> ")
            if expr_input.lower() == 'exit':
                break
            parsed_expr = parse_expression(expr_input)
            print("Parsed expression:", parsed_expr)
            result = interpret(parsed_expr)
            print("Reduced result:", result)
        except Exception as e:
            print("Error:", e)

# Example usage
if __name__ == "__main__":
    repl()

