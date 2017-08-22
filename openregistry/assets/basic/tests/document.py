# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import snitch
from openregistry.assets.basic.tests.base import (
    AssetContentWebTest
)
from openregistry.assets.basic.tests.document_blanks import (
    # AssetDocumentWithDSResourceTest
    not_found,
    create_document_in_active_asset_status,
    put_asset_document_invalid,
    patch_asset_document,
    create_asset_document_error,
    create_asset_document_json_invalid,
    create_asset_document_json,
    put_asset_document_json
)


class AssetDocumentWithDSResourceTest(AssetContentWebTest):
    docservice = True

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'

    test_create_asset_document_json = snitch(create_asset_document_json)
    test_put_asset_document_json = snitch(put_asset_document_json)
    test_patch_asset_document = snitch(patch_asset_document)

    test_not_found = snitch(not_found)
    test_create_document_active_status = snitch(create_document_in_active_asset_status)
    test_create_asset_document_error = snitch(create_asset_document_error)
    test_create_asset_document_json_invalid = snitch(create_asset_document_json_invalid)
    test_put_asset_document_invalid = snitch(put_asset_document_invalid)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
