#!/usr/bin/env python3
#
# pshub - A Pub/Sub framework implemented in Python
# Copyright (C) 2016  caizixian, lwher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from operator import lt, le, gt, ge, eq, ne, contains
from functools import wraps
import logging
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


class Rule:
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

    @staticmethod
    def from_dict(rule):
        """
        Example:
        {"level": {">=": 1, "<": 10}, "message_body": {"contains": "ERROR"}}
        :param rule: rule represented in a Python dictionary
        :return: Rule object
        """
        constraints = defaultdict(list)

        for key, value in rule.items():
            for operator, operand in value.items():
                fun = _two_partial(Rule.operators[operator], operand)
                constraints[key].append(fun)

        return Rule(constraints=constraints)

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
        logging.debug("Matching {}".format(msg))
        for k, v in msg.items():
            for fun in self.constraints[k]:
                if not fun(v):
                    logging.debug("Doesn't match")
                    return False
        logging.debug("Matches")
        return True
