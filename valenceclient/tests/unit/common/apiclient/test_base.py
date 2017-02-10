import mock

from oslotest import base as test_base
from valenceclient.common.apiclient import base

class CrudResource(base.Resource):
    pass

class CrudResourceManager(base.CrudManager):
    """Manager class for manipulating Identity crud_resources."""
    resource_class = CrudResource
    collection_key = 'crud_resources'
    key = 'crud_resource'

    def get(self, crud_resource):
        return super(CrudResourceManager, self).get(
            crud_resource_id=base.getid(crud_resource))


class ResourceTest(test_base.BaseTestCase):
    def test_reource_repr(self):
        r = base.Resource(None, dict(foo='bar', baz='spam'))
        self.assertEqual('<Resource baz=spam, foo=bar>', repr(r))

    def test_getid(self):
        class TmpObject(base.Resource):
            id = '4'
        self.assertEqual('4', base.getid(TmpObject(None, {})))
