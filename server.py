import asyncio

from viam.rpc.server import Server

from simple import Simple
from ouster_lidar import OusterLidar


async def main():
    srv = Server([Simple('simple-comp'), OusterLidar('ouster-lidar-comp')])
    await srv.serve()

if __name__ == "__main__":
    asyncio.run(main())
