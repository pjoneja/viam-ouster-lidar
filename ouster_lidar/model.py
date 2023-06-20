from typing import ClassVar, Mapping

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from .driver import OusterLidar


class MyOusterLidar(OusterLidar, Reconfigurable):
    """Inherits from ``OusterLidar`` and also conforms to the ``Reconfigurable`` protocol
    Specifies a function ``MyOusterLidar.new`` which conforms to the ``resources.types.ResourceCreator`` type.
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("pj", "demo"), "myousterlidar")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        ouster_lidar = cls(config.name)
        return ouster_lidar

    @classmethod
    def validate_config(cls, config: ComponentConfig):
        fields = config.attributes.fields
        if "sensor_hostname" not in fields:
            raise ValueError("`sensor_hostname` attribute is required")
        if "lidar_port" in fields and not isinstance(fields["lidar_port"], int):
            raise ValueError("`lidar_port` must be an integer representing the UDP port receiving lidar packets")
        if "imu_port" in fields and not isinstance(fields["imu_port"], int):
            raise ValueError("`imu_port` must be an integer representing the UDP port receiving IMU packets")
