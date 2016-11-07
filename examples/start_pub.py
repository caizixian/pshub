import asyncio
import logging
from plumbum.networking.pub import PubProtocol

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
