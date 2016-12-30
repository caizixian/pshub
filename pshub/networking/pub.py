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


class PubProtocol(asyncio.Protocol):
    def __init__(self, loop, msg_gen):
        self.loop = loop
        self.msg_gen = msg_gen
        self.rest = bytearray()
        self.count = 0

    def publish_message(self):
        msg = self.msg_gen.next(self.loop)
        logging.debug("Publishing message: {}".format(msg))
        self.transport.write(prepare_stream(make_message('pub', msg)))

    def connection_made(self, transport):
        self.transport = transport
        self.publish_message()

    def data_received(self, data):
        msgs, rest = parse_stream(self.rest, data)
        self.rest = rest
        for ty, body in msgs:
            if ty == 'rep':
                if body["succeeded"]:
                    self.count += 1
                    logging.info(
                        "Successfully published {} messages".format(self.count))
                else:
                    logging.warning("A previous publishing failed.")
            else:
                logging.warning(
                    "Invalid message type: {} from server".format(ty))

        self.publish_message()
