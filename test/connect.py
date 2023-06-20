import asyncio

import numpy as np
import open3d as o3d

from viam.robot.client import RobotClient
from viam.rpc.dial import DialOptions
from viam.components.camera import Camera
from viam.media.video import CameraMimeType


async def main():
    opts = RobotClient.Options(dial_options=DialOptions(insecure=True))
    async with await RobotClient.at_address('localhost:9090', opts) as robot:
        print("Resources\n", robot.resource_names)  # I see duplicate resources. Feels wrong!

        mock_camera: Camera = Camera.from_robot(robot, "simple-comp")  # type: ignore
        await _show_image(mock_camera)
        await _show_point_cloud(mock_camera)

        ouster_lidar: Camera = Camera.from_robot(robot, "ouster-lidar-comp")  # type: ignore
        await _show_image(ouster_lidar)
        await _show_point_cloud(ouster_lidar)


async def _show_image(camera: Camera):
    """Shows an image from the specified camera. Reusable for any supported Camera, e.g. mock or Ouster lidar"""
    image = await camera.get_image(CameraMimeType.JPEG)
    image.show()


async def _show_point_cloud(camera: Camera):
    """Shows a point cloud from the specified camera. Reusable for any supported Camera, e.g. mock or Ouster lidar"""
    pcd_bytes, _ = await camera.get_point_cloud()
    with open("tmp.pcd", "wb") as f:
        f.write(pcd_bytes)
    pcd = o3d.io.read_point_cloud("tmp.pcd")  # type: ignore
    points = np.asarray(pcd.points)
    print(points)

asyncio.run(main())
