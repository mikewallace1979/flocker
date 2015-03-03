"""
Tests for ``flocker.node.agents.blockdevice``.
"""
from zope.interface.verify import verifyObject

from ..blockdevice import (
    BlockDeviceDeployer, LoopbackBlockDeviceAPI, IBlockDeviceAPI)

from ..._deploy import IDeployer

from twisted.python.filepath import FilePath
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

    def test_list_volume_empty(self):
        """
        ``list_volumes`` returns an empty ``list`` if no block devices have
        been created.
        """
        self.assertEqual([], self.api.list_volumes())


def make_iblockdeviceapi_tests(blockdevice_api_factory):
    """
    """
    class Tests(IBlockDeviceAPITestsMixin, SynchronousTestCase):
        """
        """
        def setUp(self):
            self.api = blockdevice_api_factory(test_case=self)

    return Tests


def loopbackblockdeviceapi_for_test(test_case):
    """
    """
    root_path = FilePath(test_case.mktemp())
    return LoopbackBlockDeviceAPI(root_path=root_path)


class LoopbackBlockDeviceAPITests(
        make_iblockdeviceapi_tests(blockdevice_api_factory=loopbackblockdeviceapi_for_test)
):
    """
    Tests for ``LoopbackBlockDeviceAPITests``.
    """
