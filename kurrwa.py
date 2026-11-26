BINARY_PREC = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2}
UNARY_OPS = ('u+', 'u-')
PREC = {**BINARY_PREC, 'u+': 3, 'u-': 3}


def _is_number(token):
    try:
        float(token)
        return True
    except ValueError:
        return False


def tokenize(expression):
    tokens = []
    i, n = 0, len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif (
            ch.isdigit()
        ):
            j, dots = i, 0
            while j < n and (expression[j].isdigit() or expression[j] == '.'):
                if expression[j] == '.':
                    dots += 1
                    if dots > 1:
                        raise ValueError(
                            f"Некорректное число: {expression[i:j + 1]}"
                        )
                j += 1
            tokens.append(expression[i:j])
            i = j
        elif ch in '+-*/()':
            tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Недопустимый символ: {ch!r}")
    return tokens


def to_rpn(tokens):
    if not tokens:
        return []

    output, stack = [], []
    prev_is_operand = False

    for token in tokens:
        if _is_number(token):
            if prev_is_operand:
                raise ValueError(
                    f"Пропущен оператор перед числом: {token!r}"
                )
            output.append(token)
            prev_is_operand = True
        elif token == '(':
            stack.append(token)
            prev_is_operand = False
        elif token == ')':
            if not prev_is_operand:
                raise ValueError("Пустая скобка или оператор перед ')'")
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if not stack:
                raise ValueError("Несбалансированные скобки")
            stack.pop()
            prev_is_operand = True
        else:  # оператор
            if prev_is_operand:
                op = token
            elif token in '+-':
                op = 'u' + token
            else:
                raise ValueError(f"Некорректный оператор: {token!r}")

            while stack and stack[-1] != '(':
                top = stack[-1]
                higher = PREC[top] > PREC[op]
                equal_left = PREC[top] == PREC[op] and op not in UNARY_OPS
                if higher or equal_left:
                    output.append(stack.pop())
                else:
                    break
            stack.append(op)
            prev_is_operand = False

    if not prev_is_operand:
        raise ValueError("Выражение не может заканчиваться оператором или '('")

    while stack:
        top = stack.pop()
        if top == '(':
            raise ValueError("Несбалансированные скобки")
        output.append(top)

    return output


def readInput(userInput):
    return ' '.join(to_rpn(tokenize(userInput)))


def evaluate_rpn(rpn_tokens):
    stack = []
    for token in rpn_tokens:
        if _is_number(token):
            stack.append(float(token))
        elif token in UNARY_OPS:
            if not stack:
                raise ValueError("Недостаточно операндов")
            value = stack.pop()
            stack.append(value if token == 'u+' else -value)
        else:
            if len(stack) < 2:
                raise ValueError("Недостаточно операндов")
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("Деление на ноль")
                stack.append(a / b)
            else:
                raise ValueError(f"Неизвестный оператор: {token!r}")

    if len(stack) != 1:
        raise ValueError("Некорректное выражение")
    return stack[0]


def calculate(userInput):
    """Полный конвейер: строка -> результат."""
    return evaluate_rpn(to_rpn(tokenize(userInput)))


if __name__ == '__main__':
    user_input = input("Введите выражение: ")
    rpn_str = readInput(user_input)
    print(f"ОПЗ:       {rpn_str}")
    print(f"Результат: {evaluate_rpn(rpn_str.split())}")