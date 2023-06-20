import asyncio

from viam.module.module import Module

from simple import Simple, MySimple
from ouster_lidar import OusterLidar, MyOusterLidar


async def main():
    """This function creates and starts a new module, after adding all desired resources.
    """

    module = Module.from_args()
    module.add_model_from_registry(Simple.SUBTYPE, MySimple.MODEL)
    module.add_model_from_registry(OusterLidar.SUBTYPE, MyOusterLidar.MODEL)
    await module.start()


if __name__ == "__main__":
    asyncio.run(main())
