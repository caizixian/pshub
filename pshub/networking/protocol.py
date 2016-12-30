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

import json

delimiter = b"\r\n"


def make_body(obj):
    """

    :param obj: message body, should be JSON-serializable
    :return: encoded message body
    """
    return json.dumps(obj)


def parse_body(string):
    """

    :param string: encoded message body, should be JSON-deserializable
    :return: message body
    """
    return json.loads(string)


def make_message(ty, obj):
    """

    :param ty: type of the message
    :param obj: message body, should be JSON-serializable
    :return: encoded message
    """
    types = {
        'sub': lambda x: 'sub\t' + make_body(x),
        'pub': lambda x: 'pub\t' + make_body(x),
        'rep': lambda x: 'rep\t' + make_body(x)
    }
    return types[ty](obj)


def parse_message(string):
    ty, body = string.split('\t')
    return ty, parse_body(body)


def prepare_stream(msg):
    """

    :param msg: encoded message
    :return:  properly wrapped message for transmission
    """
    return msg.encode('utf-8') + delimiter


def parse_stream(rest, data):
    """

    :param data: currently received data
    :param rest: unprocessed data from last transmission
    :return: message entities extracted from data, unprocessed data
    """
    msgs = []
    tokens = (rest + data).split(delimiter)
    for x in tokens[:-1]:
        msgs.append(parse_message(x.decode('utf-8')))
    return msgs, tokens[-1]
