import asyncio
import logging
from plumbum.networking.sub import SubProtocol

logging.basicConfig(level=logging.DEBUG)


def main():
    loop = asyncio.get_event_loop()
    host = '127.0.0.1'
    port = 8888
    rule = {"count": {">=": 8}}
    coro = loop.create_connection(
        lambda: SubProtocol(loop, lambda body: print(body), rule),
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
