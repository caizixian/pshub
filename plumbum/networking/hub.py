import asyncio
import logging
from plumbum.networking.protocol import parse_stream, prepare_stream, make_message
from plumbum.matchingengine import RuleFactory


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
                                            RuleFactory.from_dict(body))
                self.transport.write(
                    prepare_stream(make_message("rep", {"succeeded": True})))

            elif ty == "pub":
                self.clients.publish(body)
            else:
                logging.warning("Invalid message type: {} from {}".format(ty,
                                                                          self.peername))