# -*- coding: utf-8 -*-
from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT
)


test_asset_data = {
    "title": u"футляри до державних нагород",
    "assetType": "basic",
}


class BaseAssetWebTest(BaseAWT):
    initial_data = BaseAWT
    initial_auth = ('Basic', ('broker', ''))


class AssetContentWebTest(BaseAssetWebTest):
    initial_data = test_asset_data

    def setUp(self):
        super(AssetContentWebTest, self).setUp()
        self.create_asset()
