# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import snitch
from openregistry.api.tests.blanks.mixins import ResourceDocumentTestMixin
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


class AssetDocumentWithDSResourceTest(AssetContentWebTest, ResourceDocumentTestMixin):
    docservice = True

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
