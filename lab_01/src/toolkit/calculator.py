from toolkit.errors import CalculatorError


def tokenize(expression: str) -> list: 
    """
    Преобразование строки в массив чисел, скобок и операторов
    """

    if not isinstance(expression, str):
        raise CalculatorError("Expression must be a string")
    
    expression = expression.strip()
    if not expression:
        raise CalculatorError("Empty expression")

    tokens = []
    i = 0
    n = len(expression)

    while i < n:

        char = expression[i]

        if char.isspace():
            i += 1
            continue

        elif char == '/':
            if i < n - 1:
                if expression [i + 1] == "/":
                    tokens.append("//")
                    i += 2
                    continue
            tokens.append("/")
            i += 1
        
        elif char in "+-*()%":
            tokens.append(char)
            i += 1
            continue

        elif char.isdigit() or char == '.':
            token = ""
            while i < n - 1 and (expression[i + 1].isdigit() or expression[i + 1] == '.'):
                token += expression[i]
                i += 1
            token += expression[i]
            i += 1
            try:
                float(token)
            except ValueError as exc:
                raise CalculatorError(f"Expression has an invalid number: {token}") from exc
            tokens.append(float(token))

        else:
            raise CalculatorError(f"Can't use {char} in expression")
        
    return(tokens)

def rpn_conversion(tokens: list) -> list:
    """
    перевод выражения в rpn
    """
    precedence = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '//': 2,
    '%': 2,
    }
    
    output = []
    op_stack = []
 
    for token in tokens:
        if isinstance(token, float):
            output.append(token)
 
        elif token == '(':
            op_stack.append(token)
 
        elif token == ')':
            while op_stack and op_stack[-1] != '(':
                output.append(op_stack.pop())
            if op_stack:
                op_stack.pop()  
 
        else:  # оператор
            while (
                op_stack
                and op_stack[-1] != '('
                and precedence[op_stack[-1]] >= precedence[token]
            ):
                output.append(op_stack.pop())
            op_stack.append(token)
 
    while op_stack:
        output.append(op_stack.pop())
 
    return output

    
def validate(tokens: list) -> list:
    """
    Проверка на ошибки в выражении и включение унарных знаков в числа
    """

    def is_number(f): # Проверка является ли элемент числом
        try:
            float(f)
            return True
        except:
            return False

    binary_ops = {'+', '-', '*', '/', '//', '%'}

    processed_tokens = []
    i = 0
    n = len(tokens)

    while i < n: # Алгоритм включения унарных знаков в числа
        token = tokens[i]

        is_unary = False
        if token in ('+', '-'):
            if not processed_tokens or processed_tokens[-1] == '(' or processed_tokens[-1] in binary_ops:
                is_unary = True

        if is_unary:
            if i + 1 < n and is_number(tokens[i + 1]):
                num = tokens[i + 1]
                if token == '-':
                    num = -num
                processed_tokens.append(num)
                i += 2
                continue
            else:
                raise CalculatorError(f"Expected number after unary operator '{token}'")

        processed_tokens.append(token)
        i += 1

    tokens = processed_tokens

    if not tokens:
        raise CalculatorError("Expression cannot be empty")

    stack = [] # проверка на скобки
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            if not stack:
                raise CalculatorError("Unmatched closing parenthesis ')' ")
            stack.pop()

    if stack:
        raise CalculatorError("Unmatched opening parenthesis '(' ")

    if tokens[0] in binary_ops: # проверка на то не начинается ли выражение с оператора
        raise CalculatorError(f"Expression cannot start with binary operator '{tokens[0]}'")
    if tokens[-1] in binary_ops:
        raise CalculatorError(f"Expression cannot end with binary operator '{tokens[-1]}'")

    for i in range(len(tokens)): # Проверка на пустые скобки, отсутствие операторов между операндами, два оператора подряд
        curr = tokens[i]
        prev = tokens[i - 1] if i > 0 else None

        if not is_number(curr) and curr not in binary_ops and curr not in ('(', ')'):
            raise CalculatorError(f"Invalid token: '{curr}'")

        if i > 0:
            if prev == '(' and curr == ')':
                raise CalculatorError("Empty parentheses '()' found")
            if prev in binary_ops and curr in binary_ops:
                raise CalculatorError(f"Consecutive operators: '{prev}' and '{curr}'")
            if is_number(prev) and is_number(curr):
                raise CalculatorError(f"Consecutive numbers without operator: {prev} and {curr}")
            if is_number(prev) and curr == '(':
                raise CalculatorError(f"Missing operator between number {prev} and '(' ")
            if prev == ')' and is_number(curr):
                raise CalculatorError(f"Missing operator between ')' and number {curr}")
            if prev == ')' and curr == '(':
                raise CalculatorError("Missing operator between ') ('")
            if prev == '(' and curr in binary_ops:
                raise CalculatorError(f"Binary operator '{curr}' immediately following '(' ")
            if prev in binary_ops and curr == ')':
                raise CalculatorError(f"Closing parenthesis ')' immediately following operator '{prev}'")

    return tokens

def calculate(rpn_tokens):
    """
    вычисляет выражение, полученное в rpn
    """
    stack = []
 
    for token in rpn_tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            b = stack.pop()
            a = stack.pop()
 
            if token == '+':
                result = a + b
            elif token == '-':
                result = a - b
            elif token == '*':
                result = a * b
            elif token == '/':
                result = a / b
            elif token == '//':
                result = a // b
            elif token == '%':
                result = a % b
 
            stack.append(result)
 
    return stack.pop()
