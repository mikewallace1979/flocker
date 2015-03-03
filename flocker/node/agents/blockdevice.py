# -*- test-case-name: flocker.node.agents.test.test_blockdevice -*-

"""
This module implements the parts of a block-device based dataset
convergence agent that can be re-used against many different kinds of block
devices.
"""
from uuid import uuid4

from zope.interface import implementer, Interface

from characteristic import attributes

from twisted.python.filepath import FilePath

from .. import IDeployer


class IBlockDeviceAPI(Interface):
    """
    """

    def create_volume(size):
        """
        """

    def attach_volume():
        """
        """

    def list_volumes():
        """
        """

@attributes(['blockdevice_id', 'size'])
class BlockDeviceVolume(object):
    """
    """


@implementer(IBlockDeviceAPI)
@attributes(['root_path'])
class LoopbackBlockDeviceAPI(object):
    """
    """
    unattached_directory = None

    @classmethod
    def from_path(cls, root_path):
        """
        """
        api = cls(root_path=FilePath(root_path))
        api._initialise_directories()
        return api

    def _initialise_directories(self):
        """
        """
        self._unattached_directory = self.root_path.child('unattached')
        self._unattached_directory.makedirs()

    def create_volume(self, size):
        """
        * create a file of some size (maybe size is required parameter)
        * put it in the IaaS's "unattached" directory
        """
        volume = BlockDeviceVolume(
            blockdevice_id=bytes(uuid4()).encode('ascii'),
            size=size
        )
        self._unattached_directory.child(
            volume.blockdevice_id
        ).setContent(b'\0' * volume.size)
        return volume

    def attach_volume(self):
        """
        * move file into per-host (eg named after node ip) directory
        """

    def list_volumes(self):
        """
        * list all files in "unattached" directory and all per-host directories
        """
        volumes = []
        for child in self.root_path.child('unattached').children():
            volume = BlockDeviceVolume(
                blockdevice_id=child.basename().decode('ascii'),
                size=child.getsize(),
            )
            volumes.append(volume)
        return volumes


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
