import asyncio
import logging
from plumbum.networking.protocol import parse_stream, prepare_stream, \
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
