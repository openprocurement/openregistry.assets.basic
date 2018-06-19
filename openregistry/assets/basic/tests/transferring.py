# -*- coding: utf-8 -*-
import unittest

from openregistry.assets.basic.tests.base import AssetTransferWebTest
from openregistry.assets.core.tests.plugins.transferring.mixins import AssetOwnershipChangeTestCaseMixin

class AssetOwnershipChangeTest(AssetTransferWebTest,
                               AssetOwnershipChangeTestCaseMixin):
    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetOwnershipChangeTest))
    return suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
