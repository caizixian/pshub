#!/usr/bin/env python3
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
