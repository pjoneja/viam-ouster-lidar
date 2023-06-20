"""
Register the Ouster lidar with the Viam Registry
"""

from viam.components.camera.service import CameraRPCService
from viam.components.camera.client import CameraClient
from viam.resource.registry import Registry, ResourceCreatorRegistration, ResourceRegistration
from .driver import OusterLidar
from .model import MyOusterLidar

Registry.register_subtype(ResourceRegistration(OusterLidar,
                                               CameraRPCService,
                                               lambda name, channel: CameraClient(name, channel)))

Registry.register_resource_creator(OusterLidar.SUBTYPE,
                                   MyOusterLidar.MODEL,
                                   ResourceCreatorRegistration(MyOusterLidar.new, MyOusterLidar.validate_config))

