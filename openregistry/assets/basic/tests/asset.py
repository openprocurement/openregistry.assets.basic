# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch
from openregistry.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.basic.tests.base import (
    test_asset_basic_data, BaseAssetWebTest
)
from openregistry.assets.basic.tests.asset_blanks import (
    # AssetTest
    simple_add_asset
)


class AssetBasicTest(BaseWebTest):
    initial_data = test_asset_basic_data
    relative_to = os.path.dirname(__file__)

    test_simple_add_asset = snitch(simple_add_asset)


class AssetBasicResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    initial_status = 'pending'


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetBasicResourceTest))
    tests.addTest(unittest.makeSuite(AssetBasicTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
