from valenceclient.common.apiclient import exceptions
from valenceclient.common.i18n import _

from valenceclient.common import cliutils
from valenceclient.common import utils
from valenceclient.v1 import resource_field as res_fields


def do_node_list(cc, args=None):
    """List all nodes"""
    nodes = cc.node.list()
    cliutils.print_list(nodes,fields=res_fields.NODE_RESOURCE.fields)


@cliutils.arg(
    '--memory',
    metavar='<memory>',
    help='The minimum memoery for compose a new node, the unit is MB'
)
@cliutils.arg(
    '--cpu',
    metavar='<cpu>',
    help="The cpu numbers for compose a new node"
)
@cliutils.arg(
    '--storage',
    metavar='<storage>',
    help="The remote iscsi storage, the unit is GB"
)
def do_node_compose(cc, args=None):
    """Compose a nodes"""
    field_list = ['bmcmac','ram','storage','uuid','nw',
                  'systemurl','location','bmcip','cpu','id']
    params = {}

    if args.memory is not None:
        params['Memory'] = [{'CapacityMiB':args.memory}]
    if args.cpu is not None:
        params['Processors'] = [{'TotalCores':args.cpu}]
    if args.storage is not None:
        params['RemoteDrives'] = [{'CapacityGiB':args.storage,
                                   'iSCSIAddress':
                                       'iqn.2016-09.com.openstack:storage.disk'}]

    node = cc.node.compose(**params)
    id = node.node.split('/')[-1]
    info = cc.node.get(id)
    data = dict((i, getattr(info, i, "")) for i in field_list)
    cliutils.print_dict(data, wrap=72)



@cliutils.arg(
    'node',
    metavar='<id>',
    help="ID of the node")
def do_node_show(cc, args):
    """show the detail information about the id of node"""
    field_list = ['bmcmac','ram','storage','uuid','nw',
                  'systemurl','location','bmcip','cpu','id']
    utils.check_empty_arg(args.node, '<id>')
    # The return value is dict, should be convert to list
    node = cc.node.get(args.node)
    data = dict((i, getattr(node, i, "")) for i in field_list)
    cliutils.print_dict(data, wrap=72)


@cliutils.arg(
    'node',
    metavar='<id>',
    help="ID of the node")
def do_node_delete(cc, args):
    """Delete the id of node"""
    utils.check_empty_arg(args.node, '<id>')
    # The return value is dict, should be convert to list
    n = cc.node.delete(args.node)

