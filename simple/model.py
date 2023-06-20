from typing import ClassVar, Mapping

from typing_extensions import Self

from viam.module.types import Reconfigurable
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import ResourceName
from viam.resource.base import ResourceBase
from viam.resource.types import Model, ModelFamily
from .driver import Simple


class MySimple(Simple, Reconfigurable):
    """Inherits from ``Simple`` and also conforms to the ``Reconfigurable`` protocol
    Specifies a function ``MySimple.new`` which conforms to the ``resources.types.ResourceCreator`` type.
    """

    MODEL: ClassVar[Model] = Model(ModelFamily("pj", "demo"), "mysimple")

    @classmethod
    def new(cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        return cls(config.name)

    @classmethod
    def validate_config(cls, config: ComponentConfig):
        pass
