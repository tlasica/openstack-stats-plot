from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security
import ruamel.yaml as yaml
import operator
import itertools


def initialize_session(keystone_url, user, password, tenant):
    """
    Initialized libcloud openstack driver, authenticate user
    """
    # not sure if it is required
    # libcloud.security.VERIFY_SSL_CERT = False
    OpenStack = get_driver(Provider.OPENSTACK)
    driver  = OpenStack(user, password, ex_force_auth_url=keystone_url, ex_force_auth_version='2.0_password', ex_tenant_name=tenant)
    return driver


def get_nodes_with_size(session):
    """
    List nodes in tenat with it's size for each node
    """
    nodes = session.list_nodes()
    sizes = dict( [(x.id,x) for x in session.list_sizes()] )
    return [(n, sizes[n.extra['flavorId']]) for n in nodes]


def ram_per_user(session):
    """
    List RAM usage per userId, not sorted
    """
    nodes_with_size = get_nodes_with_size(session)
    xs = [(n.extra['userId'], s.ram) for n,s in nodes_with_size]
    return sum_group(sorted(xs))


def cpu_per_user(session):
    """
    List VCPUs usage per userId, not sorted
    """
    nodes_with_size = get_nodes_with_size(session)
    xs = [(n.extra['userId'], s.vcpus) for n,s in nodes_with_size]
    return sum_group(sorted(xs))


def sum_group(xs):
  return [(key, sum(num for _, num in value)) for key, value in itertools.groupby(xs, operator.itemgetter(0))]


def read_config(config_file_path):
    with open(config_file_path, 'r') as stream:
        return yaml.safe_load(stream)

# sort by value asc
# sorted(sum_group(user_and_ram), key=operator.itemgetter(1))
# sorted(sum_group(user_and_cpu), key=operator.itemgetter(1))
