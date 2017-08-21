# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch

from openregistry.assets.basic.tests.base import (
    test_asset_data, BaseAssetWebTest
)
from openregistry.assets.basic.tests.asset_blanks import (
    # AssetResourceTest
    listing,
    get_asset,
    asset_not_found,
    dateModified_asset,
    listing_draft,
    listing_changes,
    create_asset,
    patch_asset,
    asset_concierge_patch,
    administrator_change_delete_status,
    administrator_change_complete_status,
    # AssetTest
    simple_add_asset
)


class AssetResourceTestMixin(object):
    test_01_listing = snitch(listing)
    test_02_listing_changes = snitch(listing_changes)
    test_03_listing_draft = snitch(listing_draft)
    test_04_get_asset = snitch(get_asset)
    test_05_dateModified_asset = snitch(dateModified_asset)
    test_06_asset_not_found = snitch(asset_not_found)
    test_07_create_asset = snitch(create_asset)
    test_08_patch_asset = snitch(patch_asset)
    test_09_asset_concierge_patch = snitch(asset_concierge_patch)
    test_10_administrator_change_delete_status = snitch(administrator_change_delete_status)
    test_11_administrator_change_complete_status = snitch(administrator_change_complete_status)


class AssetTest(BaseWebTest):
    initial_data = test_asset_data
    relative_to = os.path.dirname(__file__)

    test_simple_add_asset = snitch(simple_add_asset)


class AssetResourceTest(BaseAssetWebTest, AssetResourceTestMixin):
    initial_status = 'pending'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetResourceTest))
    suite.addTest(unittest.makeSuite(AssetTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
