from dataclasses import dataclass
from typing import Callable, Union, Dict


# def simple_example(cmd):
#     match cmd:
#         case "ls": print("Listing dir")
#         case ["ls", x] if isinstance(x, int): print(f"Listing in {x}")
#         case _ : print("haha")
#
#
# simple_example("ls")
# simple_example("ls1")
# simple_example(["ls", 12])
# simple_example(["ls", "s"])


@dataclass
class Number:
    val: int


@dataclass
class Variable:
    name: str


EvalFun = Callable[[int, int], int]


@dataclass
class Operator:
    name: str
    eval_fun: EvalFun

    def __call__(self, x1: int, x2: int) -> int:
        return self.eval_fun(x1, x2)


@dataclass
class OperatorNode:
    operator: Operator
    left: "Expression"
    right: "Expression"


Expression = Union[Number, Variable, OperatorNode, int]

operators = [
    Operator(n, o) for (n, o) in
    [
        ("+", lambda x, y: x + y),
        ("-", lambda x, y: x - y),
        ("*", lambda x, y: x * y),
        ("/", lambda x, y: x / y),
    ]
]
State = Dict[str, int]


def evaluate(state: State, expr: Expression):
    if isinstance(expr, Number):
        return expr.val
    elif isinstance(expr, Variable):
        return state[expr.name]
    elif isinstance(expr, OperatorNode):
        left = evaluate(state, expr.left)
        right = evaluate(state, expr.right)
        return expr.operator(left, right)


def evaluate2(state: State, expr: Expression):
    match expr:
        case Number(x) | x if isinstance(x, int):
            return x
        case Variable(name=name):
            return state[name]
        case OperatorNode(op, left, right):
            left = evaluate2(state, left)
            right = evaluate2(state, right)
            return op(left, right)
    # if isinstance(expr, Number):
    #     return expr.val
    # elif isinstance(expr, Variable):
    #     return state[expr.name]
    # elif isinstance(expr, OperatorNode):
    #     left = evaluate2(state, expr.left)
    #     right = evaluate2(state, expr.right)
    #     return expr.operator(left, right)


sample = OperatorNode(operators[1],
                      OperatorNode(operators[0],
                                   Variable("x"),
                                   Number(10)),
                      100)

env = {"x": 15}

print(evaluate2(env, sample))
