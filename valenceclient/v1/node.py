
from valenceclient.common import base

class Node(base.Resource):
    def __repr__(self):
        return "<Node %s" % self._info


class NodeManager(base.CreateManager):
    resource_class = Node
    _resource_name = 'nodes'
    _creation_attributes = ['Processors', 'RemoteDrives', 'Memory']

    def list(self, resource_class=None):

        nodes = self._list(self._path(),resource_class if resource_class else self.resource_class)
        return nodes

    def get(self, node_id):
        return self._get(node_id)

    def delete(self, node_id):
        return self._delete(node_id)

    def update(self, node_id, patch, http_method='PATCH'):
        return self._update(resource_id=node_id, patch=patch,
                            method=http_method)
    def compose(self, **kwargs):
        return  self.create(**kwargs)




