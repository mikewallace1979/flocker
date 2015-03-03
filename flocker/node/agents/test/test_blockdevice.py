"""
Tests for ``flocker.node.agents.blockdevice``.
"""
from zope.interface.verify import verifyObject

from ..blockdevice import (
    BlockDeviceDeployer, LoopbackBlockDeviceAPI, IBlockDeviceAPI)

from ..._deploy import IDeployer

from twisted.trial.unittest import SynchronousTestCase


class BlockDeviceDeployerTests(SynchronousTestCase):
    def test_interface(self):
        """
        ``BlockDeviceDeployer`` instances provide ``IDeployer``.
        """
        self.assertTrue(
            verifyObject(IDeployer, BlockDeviceDeployer())
        )


class LoopbackBlockDeviceAPITests(SynchronousTestCase):
    """
    """
    def test_interface(self):
        """
        ``LoopbackBlockDeviceAPI`` instances provide ``IBlockDeviceAPI``.
        """
        self.assertTrue(
            verifyObject(IBlockDeviceAPI, LoopbackBlockDeviceAPI())
        )
