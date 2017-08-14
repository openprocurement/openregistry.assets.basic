# -*- coding: utf-8 -*-
import os
import unittest

from openregistry.api.tests.base import snitch
from openregistry.assets.basic.tests.base import (
    AssetContentWebTest
)
from openregistry.assets.basic.tests.document_blanks import (
    # AssetDocumentResourceTest
    not_found,
    create_document_active_tendering_status,
    create_tender_document,
    put_tender_document,
    patch_tender_document,
    # AssetDocumentWithDSResourceTest
    create_tender_document_error,
    create_tender_document_json_invalid,
    create_tender_document_json,
    put_tender_document_json
)


class AssetDocumentResourceTestMixin(object):
    forbidden_document_modification_actions_status = 'active'  # status, in which operations with tender documents (adding, updating) are forbidden

    test_not_found = snitch(not_found)
    test_create_tender_document = snitch(create_tender_document)
    test_put_tender_document = snitch(put_tender_document)
    test_patch_tender_document = snitch(patch_tender_document)


class AssetDocumentWithDSResourceTestMixin(object):
    test_create_tender_document_json_invalid = snitch(create_tender_document_json_invalid)
    test_create_tender_document_json = snitch(create_tender_document_json)
    test_put_tender_document_json = snitch(put_tender_document_json)


class AssetDocumentResourceTest(AssetContentWebTest, AssetDocumentResourceTestMixin):
    relative_to = os.path.dirname(__file__)

    test_create_document_active_tendering_status = snitch(create_document_active_tendering_status)


class AssetDocumentWithDSResourceTest(AssetDocumentResourceTest, AssetDocumentWithDSResourceTestMixin):
    docservice = True
    relative_to = os.path.dirname(__file__)

    test_create_tender_document_error = snitch(create_tender_document_error)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetDocumentResourceTest))
    suite.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
