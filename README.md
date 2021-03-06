# pshub
`pshub` is a lightweight Python framework that partially implements Publish/Subscribe messaging paradigm. 

It utilizes `asyncio` library to support concurrent requests handling. The Python version that we recommend is 3.5+ .

## Name

The name `pshub` indicates the three main components of this library — Pub, Sub and Hub.

## Usage

You can refer to the three example files under directory `examples/`.

## Cheatsheet

### Rule

#### Example

`{"level": {">=": 1, "<": 10}, "message_body": {"contains": "ERROR"}}`

#### Valid Operators

- `contains`
- `<`
- `<=`
- `>`
- `>=`
- `=`
- `!=`
- `excludes`

### Message

#### Example

`{"level": 2, "message_body": "ERROR occurs"}`

## Caveats

- All messages/rules should be Python `dict` whose keys and values are primitive Python type (int, string, etc.)

- The second parameter of the constructor of `PubProtocol`, `msg_gen`, should has following method:

```python
class MessageGenerator(object):
    def next(self, loop):
        """
        Return next message 
        
        Stop the loop if there's no message to publish.
        """
        pass
```

## License

Plumbum - A Pub/Sub framework implemented in Python
Copyright (C) 2016  caizixian, lwher

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
