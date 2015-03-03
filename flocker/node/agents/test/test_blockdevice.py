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


class IBlockDeviceAPITestsMixin(object):
    """
    """
    def test_interface(self):
        """
        ``api`` instances provide ``IBlockDeviceAPI``.
        """
        self.assertTrue(
            verifyObject(IBlockDeviceAPI, self.api)
        )

    def test_list_volume(self):
        """
        ``create_volume``
        """


def make_iblockdeviceapi_tests(blockdevice_api_type):

    class Tests(IBlockDeviceAPITestsMixin, SynchronousTestCase):
        """
        """
        def setUp(self):
            self.api = blockdevice_api_type()

    return Tests


class LoopbackBlockDeviceAPITests(
        make_iblockdeviceapi_tests(blockdevice_api_type=LoopbackBlockDeviceAPI)
):
    """
    Tests for ``LoopbackBlockDeviceAPITests``.
    """
