from typing import Final, Iterable, Optional, Tuple

import numpy as np
from PIL import Image

from ouster import client
from viam.components.camera import Camera
from viam.resource.types import RESOURCE_TYPE_COMPONENT, Subtype


class OusterLidar(Camera):

    SUBTYPE: Final = Subtype("pj", RESOURCE_TYPE_COMPONENT, "ouster_lidar")  # overriding a Final feels illegal?

    def __init__(self, name: str):
        self.source = client.Sensor("os-122247000765.local", lidar_port=7502, imu_port=7503)
        self.scans = iter(client.Scans(self.source, complete=True))
        self.metadata = self.source.metadata
        self.xyz_lut = client.XYZLut(self.metadata)  # pre-compute lookup table for calculating XYZ from depth
        super().__init__(name)

    def __del__(self):
        if self.source:
            self.source.close()

    async def get_image(self, mime_type: str = "", *, timeout: Optional[float] = None, **kwargs) -> Image:
        self.source.flush()  # flush old packets, only look at newest data
        scan: client.LidarScan = next(self.scans)
        array_2d = scan.field(client.ChanField.REFLECTIVITY)
        array_2d = array_2d.astype(np.uint32)  # must be uint8, int32 or float for PIL
        array_2d = client.destagger(self.metadata, array_2d)
        return Image.fromarray(array_2d).convert('RGB')

    async def get_point_cloud(self, *, timeout: Optional[float] = None, **kwargs) -> Tuple[bytes, str]:
        scan: client.LidarScan = next(self.scans)
        xyz = self.xyz_lut(scan.field(client.ChanField.RANGE))
        pcd = o3d.geometry.PointCloud()  # type: ignore
        pcd.points = o3d.utility.Vector3dVector(xyz.reshape(-1, 3))  # type: ignore
        return pcd, "what is the MIME type of a PCD???"

    async def get_properties(self, *, timeout: Optional[float] = None, **kwargs) -> Camera.Properties:
        pass
