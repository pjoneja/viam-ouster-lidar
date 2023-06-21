from pathlib import Path
from typing import Final, Optional, Tuple

from PIL import Image

from viam.components.camera import Camera
from viam.resource.types import RESOURCE_TYPE_COMPONENT, Subtype


class Simple(Camera):

    SUBTYPE: Final = Subtype("pj", RESOURCE_TYPE_COMPONENT, "simple")  # overriding a Final feels illegal?

    def __init__(self, name: str):
        directory = Path(__file__).parent.absolute()  # path to directory containing this python file
        self.image = Image.open(directory / "room.jpg")
        with open(directory / "room_0.pcd", mode="rb") as pcd_file:
            self.pcd = pcd_file.read()
        super().__init__(name)

    def __del__(self):
        self.image.close()

    async def get_image(self, mime_type: str = "", *, timeout: Optional[float] = None, **kwargs) -> Image:
        return self.image.copy()

    async def get_point_cloud(self, *, timeout: Optional[float] = None, **kwargs) -> Tuple[bytes, str]:
        return self.pcd, "pointcloud/pcd"

    async def get_properties(self, *, timeout: Optional[float] = None, **kwargs) -> Camera.Properties:
        pass

