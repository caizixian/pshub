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
from pshub.matchingengine import Rule


class HubClients(object):
    def __init__(self):
        self.subscribers = {}

    def add_subscriber(self, peername, transport, rule):
        self.subscribers[peername] = (transport, rule)

    def publish(self, msg):
        for transport, rule in self.subscribers.values():
            if rule.match(msg):
                transport.write(prepare_stream(make_message("pub", msg)))


class HubProtocol(asyncio.Protocol):
    def __init__(self, loop, clients):
        self.loop = loop
        self.clients = clients
        self.rest = bytearray()

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        logging.info("Connection from {}".format(self.peername))

    def data_received(self, data):
        msgs, rest = parse_stream(self.rest, data)
        self.rest = rest
        for ty, body in msgs:
            if ty == "sub":
                self.clients.add_subscriber(self.peername, self.transport,
                                            Rule.from_dict(body))
                self.transport.write(
                    prepare_stream(make_message("rep", {"succeeded": True})))

            elif ty == "pub":
                self.clients.publish(body)
                self.transport.write(
                    prepare_stream(make_message("rep", {"succeeded": True})))
            else:
                logging.warning("Invalid message type: {} from {}".format(ty,
                                                                          self.peername))
