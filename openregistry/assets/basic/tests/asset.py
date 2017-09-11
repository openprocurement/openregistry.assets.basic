# -*- coding: utf-8 -*-
import unittest

from openregistry.api.tests.blanks.mixins import ResourceTestMixin

from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.basic.models import Asset as AssetBasic
from openregistry.assets.basic.tests.base import (
    test_asset_basic_data, BaseAssetWebTest
)


class AssetBasicResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetBasic
    initial_data = test_asset_basic_data
    initial_status = 'pending'


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetBasicResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
