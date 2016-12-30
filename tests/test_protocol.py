from pshub.networking.protocol import *
import json

sample_rule = {"level": {">=": 1, "<": 10},
               "message_body": {"contains": "ERROR"}}
sample_msg = {"level": 2, "message_body": "ERROR occurs"}


def test_make_body():
    assert make_body(sample_rule) == json.dumps(sample_rule)
    assert make_body(sample_msg) == json.dumps(sample_msg)


def test_parse_body():
    assert parse_body(make_body(sample_rule)) == sample_rule
    assert parse_body(make_body(sample_msg)) == sample_msg


def test_make_message():
    msg = make_message("sub", sample_rule)
    assert "\t" in msg
    assert "sub", make_body(sample_rule) == msg.split("\t")


def test_parse_message():
    assert parse_message(make_message("sub", sample_rule))[0] == "sub"
    assert parse_message(make_message("sub", sample_rule))[1] == sample_rule


def test_prepare_stream():
    msg = make_message("sub", sample_rule)
    assert prepare_stream(msg) == msg.encode('utf-8') + b"\r\n"


def test_parse_stream():
    msg = make_message("sub", sample_rule)
    stream = prepare_stream(msg)
    assert parse_stream(bytearray(), stream)[0][0][0] == "sub"
    assert parse_stream(bytearray(), stream)[0][0][1] == sample_rule
    assert not parse_stream(bytearray(), stream)[1]
    assert parse_stream(bytearray(), stream + b" extra")[1] == b" extra"
    assert parse_stream(stream[0:5], stream[5:] + b"extra")[0][0][0] == "sub"
    assert parse_stream(stream[0:5], stream[5:] + b"extra")[1] == b"extra"
