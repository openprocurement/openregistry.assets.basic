# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import BaseWebTest, snitch

from openregistry.assets.basic.tests.base import (
    test_asset_data, BaseAssetWebTest
)
from openregistry.assets.basic.tests.asset_blanks import (
    # TenderResourceTest
    listing,
    get_asset,
    asset_not_found,
    dateModified_asset,
    listing_draft,
    listing_changes,
    create_asset,
    patch_asset,
    # TenderTest
    simple_add_asset,
)


class TenderResourceTestMixin(object):
    test_listing_changes = snitch(listing_changes)
    test_listing_draft = snitch(listing_draft)
    test_listing = snitch(listing)
    test_create_asset = snitch(create_asset)
    test_get_asset = snitch(get_asset)
    test_dateModified_asset = snitch(dateModified_asset)
    test_asset_not_found = snitch(asset_not_found)


class TenderTest(BaseWebTest):
    initial_data = test_asset_data
    relative_to = os.path.dirname(__file__)

    test_simple_add_asset = snitch(simple_add_asset)


class TenderResourceTest(BaseAssetWebTest, TenderResourceTestMixin):
    initial_data = test_asset_data
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderResourceTest))
    suite.addTest(unittest.makeSuite(TenderTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
