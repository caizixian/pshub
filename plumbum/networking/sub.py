import asyncio

from plumbum.networking.protocol import parse_stream, prepare_stream, make_message

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
        for ty, body in msgs:
            if ty == 'pub':
                self.callback(body)
            elif ty == 'rep':
                logging.info("Update successfully")
            else:
                logging.warning("Invalid message type: {} from server".format(ty))
