
from valenceclient.common import base
from valenceclient.common.i18n import _
from valenceclient.common import utils
from valenceclient import exc

class Chassis(base.Resource):
    def __repr__(self):
        return "<Chassis %s" % self._info


class ChassisManager(base.CreateManager):
    resource_class = Chassis
    _resource_name = 'chassis'
    _creation_attributes = []

    def list(self):
        pass


    def get(self):
        pass

    def delete(self):
        pass
