# -*- test-case-name: flocker.node.agents.test.test_blockdevice -*-

"""
This module implements the parts of a block-device based dataset
convergence agent that can be re-used against many different kinds of block
devices.
"""

from zope.interface import implementer, Interface

from characteristic import attributes

from .. import IDeployer


class IBlockDeviceAPI(Interface):
    """
    """

    def create_volume():
        """
        """

    def attach_volume():
        """
        """

    def list_volumes():
        """
        """


@implementer(IBlockDeviceAPI)
@attributes(['root_path'])
class LoopbackBlockDeviceAPI(object):
    """
    """
    def create_volume(self):
        """
        * create a file of some size (maybe size is required parameter)
        * put it in the IaaS's "unattached" directory
        """

    def attach_volume(self):
        """
        * move file into per-host (eg named after node ip) directory
        """

    def list_volumes(self):
        """
        * list all files in "unattached" directory and all per-host directories
        """
        return []


@implementer(IDeployer)
# @attributes(["hostname", "block_device_api"])
class BlockDeviceDeployer(object):
    """
    """
    def discover_local_state(self):
        """
        """

    def calculate_necessary_state_changes(self, local_state,
                                          desired_configuration,
                                          current_cluster_state):
        """
        """
