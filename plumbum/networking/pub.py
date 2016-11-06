import asyncio

from plumbum.networking.protocol import parse_stream, prepare_stream, make_message

class PubProtocol(asyncio.Protocol):
    def __init__(self, loop, msg):
        self.loop = loop
        self.msg = msg
        self.case = 0
        
    def connection_made(self, transport):
        self.transport = transport
        transport.write(prepare_stream(make_message('pub', self.msg.next())))     

    def data_received(self, data):
        self.case += 1
        logging.info("Publish {} successfully".format(str(self.case)))
        self.transport.write(prepare_stream(make_message('pub', self.msg.next()))
