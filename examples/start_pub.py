#!/usr/bin/env python3
#
# Plumbum - A Pub/Sub framework implemented in Python
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

import asyncio
import logging
from plumbum import PubProtocol

logging.basicConfig(level=logging.DEBUG)


class MessageGenerator(object):
    def __init__(self):
        self.count = 0

    def next(self, loop):
        msg = {"count": self.count}
        self.count += 1
        if self.count >= 36:
            loop.stop()
        return msg


def main():
    loop = asyncio.get_event_loop()
    host = '127.0.0.1'
    port = 8888

    coro = loop.create_connection(lambda: PubProtocol(loop, MessageGenerator()),
                                  host,
                                  port)

    loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    loop.close()


if __name__ == "__main__":
    main()
