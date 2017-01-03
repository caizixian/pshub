def test_operators():
    from pshub.matchingengine.rule import Rule
    operators = Rule.operators
    assert operators["contains"]("abc", "a")
    assert not operators["contains"]("abc", "z")
    assert operators["contains"]([1, 2, 3], 1)
    assert not operators["contains"]([1, 2, 3], 233)

    assert operators["<"](1, 2)
    assert operators["<="](1, 1)
    assert operators["<="](1, 2)

    assert not operators[">"](1, 2)
    assert operators[">="](2, 2)
    assert operators[">="](3, 2)

    assert operators["="](1, 1)
    assert operators["="](None, None)
    assert operators["="]("a", "a")
    assert operators["="]({1, 2, 3}, {3, 2, 1})

    assert operators["!="](1, 2)

    assert not operators["excludes"]([1, 2, 3], 1)


def test_rule():
    from pshub.matchingengine.rule import Rule
    sample_rule = {"level": {">=": 1, "<": 10},
                   "message_body": {"contains": "ERROR"}}
    rule = Rule.from_dict(sample_rule)
    assert rule.match({"level": 3, "message_body": "ERROR CODE 1"})
    assert not rule.match({"level": 10, "message_body": "ERROR CODE 1"})
    assert not rule.match({"level": 3, "message_body": "WARNING"})
