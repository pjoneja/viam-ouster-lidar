"""
Register the simple camera with the Viam Registry
"""

from viam.components.camera.service import CameraRPCService
from viam.components.camera.client import CameraClient
from viam.resource.registry import Registry, ResourceCreatorRegistration, ResourceRegistration
from .driver import Simple
from .model import MySimple

Registry.register_subtype(ResourceRegistration(Simple,
                                               CameraRPCService,
                                               lambda name, channel: CameraClient(name, channel)))

Registry.register_resource_creator(Simple.SUBTYPE,
                                   MySimple.MODEL,
                                   ResourceCreatorRegistration(MySimple.new, MySimple.validate_config))

