import asyncio
import logging
from plumbum.networking.hub import HubProtocol, HubClients

logging.basicConfig(level=logging.DEBUG)


def main():
    loop = asyncio.get_event_loop()
    host = '127.0.0.1'
    port = 8888
    clients = HubClients()
    coro = loop.create_server(lambda: HubProtocol(loop, clients), host,
                              port)
    server = loop.run_until_complete(coro)

    logging.info('Serving on {}'.format(server.sockets[0].getsockname()))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    main()
