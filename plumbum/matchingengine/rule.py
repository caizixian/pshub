#!/usr/bin/env python3
from operator import lt, le, gt, ge, eq, ne, contains
from functools import wraps
import json
from collections import defaultdict


def my_not(f):
    @wraps(f)
    def foo(*args, **kwargs):
        return not f(*args, **kwargs)

    return foo


def two_partial(func, second_param):
    def fun(first_param):
        return func(first_param, second_param)

    return fun


class RuleFactory:
    operators = {
        "contains": contains,
        "<": lt,
        "<=": le,
        ">": gt,
        ">=": ge,
        "=": eq,
        "!=": ne,
        "excludes": my_not(contains)
    }

    def __init__(self):
        pass

    @staticmethod
    def from_string(rule_str):
        parsed_rule = json.loads(rule_str)
        constraints = defaultdict(list)

        for key, value in parsed_rule.items():
            for operator, operand in value.items():
                fun = two_partial(RuleFactory.operators[operator], operand)
                constraints[key].append(fun)

        return Rule(constraints=constraints)


class Rule:
    def __init__(self, constraints):
        self.constraints = constraints

    def match(self, msg):
        parsed_msg = json.loads(msg)

        for k, v in parsed_msg.items():
            for fun in self.constraints[k]:
                if not fun(v):
                    return False

        return True