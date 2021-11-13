import itertools
from random import randint

def get_random():
    _list = []
    nums = [1,2,3,4,5,6,8,7,9]
    for i in range(1,5):
        _list.append(nums.pop(randint(0,len(nums)-1)))
    return solve(_list),_list

def solve(numbers, goal=24, expr=[]):
    if expr == []:
        expr = [str(n) for n in numbers]
    if len(numbers) == 1:
        if numbers[0] == goal:
            return numbers[0]
        else:
            return False
    if len(numbers) == 2:
        answers, answer_exps = combinetwo(numbers[0], numbers[1])
        for i,answer in enumerate(answers):
            if answer == goal:
                return convert_expr_to_string(expr[0], expr[1], answer_exps[i])
        return False

    pairs = set(itertools.combinations(numbers, 2))
    for pair in pairs:
        possible_values, possible_expr = combinetwo(*pair)
        for counter, value in enumerate(possible_values):
            expression = possible_expr[counter]
            a_index = numbers.index(pair[0])
            b_index = numbers.index(pair[1])
            if a_index == b_index:
                b_index = numbers.index(pair[1], a_index + 1);

            expr_string = convert_expr_to_string(expr[a_index], expr[b_index], expression)
            newlist = numbers[:]
            newexpr = expr[:]
            
            # replace the two numbers with the combined result
            a_index = newlist.index(pair[0])
            newlist.pop(a_index)
            b_index = newlist.index(pair[1])
            newlist.pop(b_index)
            newlist.append(value)

            # order matters
            newexpr.pop(a_index)
            newexpr.pop(b_index)
            newexpr.append(expr_string)
            result = solve(newlist, goal, newexpr)
            if result:
                return remove_redundant_brackets(result)
            else:
                continue

def convert_expr_to_string(a, b, expr):
    temp = [a, b]
    result = '(' + str(temp[expr[0]]) + ')' + str(expr[1]) + '(' + str(temp[expr[2]]) + ')'
    return result

def combinetwo(a, b):
    result = [a + b, a * b]
    expr = [(0, '+', 1), (0, '*', 1)]
    if b > a:
        result.append(b-a)
        expr.append((1, '-', 0))
    else:
        result.append(a-b)
        expr.append((0, '-', 1))
    if b != 0:
        result.append(a / b)
        expr.append((0, '/', 1))
    if a != 0:
        result.append(b / a)
        expr.append((1, '/', 0))
    return result, expr

def remove_redundant_brackets(expr):
    stack = []
    # indices to be deleted
    indices = []
    for i, ch in enumerate(expr):
        if ch == '(':
            stack.append(i)
        if ch == ')':
            last_bracket_index = stack.pop()
            enclosed = expr[last_bracket_index + 1:i]
            if enclosed.isdigit():
                indices.append(i)
                indices.append(last_bracket_index)
    return "".join([char for idx, char in enumerate(expr) if idx not in indices])