# -*- test-case-name: flocker.node.agents.test.test_blockdevice -*-

"""
This module implements the parts of a block-device based dataset
convergence agent that can be re-used against many different kinds of block
devices.
"""
from uuid import uuid4

from zope.interface import implementer, Interface

from characteristic import attributes
from pyrsistent import PRecord, field

from twisted.internet.defer import succeed
from twisted.python.filepath import FilePath

from .. import IDeployer
from ...control import NodeState


class UnknownVolume(Exception):
    """
    """


class AlreadyAttachedVolume(Exception):
    """
    """


class IBlockDeviceAPI(Interface):
    """
    """

    def create_volume(size):
        """
        """

    def attach_volume(blockdevice_id, host):
        """
        """

    def list_volumes():
        """
        """

class BlockDeviceVolume(PRecord):
    """
    """
    blockdevice_id = field(type=bytes, mandatory=True)
    size = field(type=int, mandatory=True)
    host = field(type=(bytes, type(None)), initial=None)


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
        self._attached_directory = self.root_path.child('attached')
        self._attached_directory.makedirs()

    def create_volume(self, size):
        """
        * create a file of some size (maybe size is required parameter)
        * put it in the IaaS's "unattached" directory
        """
        volume = BlockDeviceVolume(
            blockdevice_id=bytes(uuid4()),
            size=size,
        )
        self._unattached_directory.child(
            volume.blockdevice_id
        ).setContent(b'\0' * volume.size)
        return volume

    def _get(self, blockdevice_id):
        for volume in self.list_volumes():
            if volume.blockdevice_id == blockdevice_id:
                return volume
        return None

    def attach_volume(self, blockdevice_id, host):
        """
        * move file into per-host (eg named after node ip) directory
        """
        volume = self._get(blockdevice_id)
        if volume is None:
            raise UnknownVolume()

        if volume.host is None:
            attached_volume = volume.set(host=host)
            f = self._unattached_directory.child(attached_volume.blockdevice_id)
            host_directory = self._attached_directory.child(host)
            host_directory.makedirs()
            f.moveTo(host_directory.child(f.basename()))
            return attached_volume

        raise AlreadyAttachedVolume()

    def list_volumes(self):
        """
        * list all files in "unattached" directory and all per-host directories
        """
        volumes = []
        for child in self.root_path.child('unattached').children():
            volume = BlockDeviceVolume(
                blockdevice_id=child.basename(),
                size=child.getsize(),
            )
            volumes.append(volume)

        for host_directory in self.root_path.child('attached').children():
            host_name = host_directory.basename()
            for child in host_directory.children():

                volume = BlockDeviceVolume(
                    blockdevice_id=child.basename(),
                    size=child.getsize(),
                    host=host_name
                )
                volumes.append(volume)

        return volumes


@implementer(IDeployer)
@attributes(["hostname", "block_device_api"])
class BlockDeviceDeployer(object):
    """
    """
    def discover_local_state(self):
        """
        """

        state = NodeState(
            hostname=self.hostname,
            running=frozenset(),
            not_running=frozenset()
        )
        return succeed(state)

    def calculate_necessary_state_changes(self, local_state,
                                          desired_configuration,
                                          current_cluster_state):
        """
        """
