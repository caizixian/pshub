#!/usr/bin/env python3
from operator import lt, le, gt, ge, eq, ne, contains
from functools import wraps
import json
from collections import defaultdict


def _my_not(f):
    @wraps(f)
    def foo(*args, **kwargs):
        return not f(*args, **kwargs)

    return foo


def _two_partial(func, second_param):
    def fun(first_param):
        return func(first_param, second_param)

    return fun


class RuleFactory:
    """
    RuleFactory provides methods to create Rules
    """
    operators = {
        "contains": contains,
        "<": lt,
        "<=": le,
        ">": gt,
        ">=": ge,
        "=": eq,
        "!=": ne,
        "excludes": _my_not(contains)
    }

    def __init__(self):
        pass

    @staticmethod
    def from_dict(rule):
        """
        Example:
        {"level": {">=": 1, "<": 10}, "message_body": {"contain": "ERROR"}}
        :param rule: rule represented in a Python dictionary
        :return: Rule object
        """
        parsed_rule = json.loads(rule)
        constraints = defaultdict(list)

        for key, value in parsed_rule.items():
            for operator, operand in value.items():
                fun = _two_partial(RuleFactory.operators[operator], operand)
                constraints[key].append(fun)

        return Rule(constraints=constraints)


class Rule:
    def __init__(self, constraints):
        self.constraints = constraints

    def match(self, msg):
        """
        Match message against some constraints
        Example:
        {"level": 2, "message_body": "ERROR occurs"}
        :param msg: message represented in a Python dictionary
        :return: Successfully matched or not
        """

        for k, v in msg.items():
            for fun in self.constraints[k]:
                if not fun(v):
                    return False

        return True
