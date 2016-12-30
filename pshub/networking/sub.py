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

import asyncio
import logging
from pshub.networking.protocol import parse_stream, prepare_stream, \
    make_message


class SubProtocol(asyncio.Protocol):
    def __init__(self, loop, callback, rule):
        self.loop = loop
        self.callback = callback
        self.rule = rule
        self.rest = bytearray()

    def connection_made(self, transport):
        transport.write(prepare_stream(make_message('sub', self.rule)))

    def data_received(self, data):
        msgs, rest = parse_stream(self.rest, data)
        self.rest = rest
        for ty, body in msgs:
            if ty == 'pub':
                self.callback(body)
            elif ty == 'rep':
                if body["succeeded"]:
                    logging.info("Successfully subscribe at a hub.")
                else:
                    logging.warning("Failed to subscribe at a hub.")

            else:
                logging.warning(
                    "Invalid message type: {} from server".format(ty))
