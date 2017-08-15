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
)


class AssetDocumentResourceTestMixin(object):

    test_not_found = snitch(not_found)
    test_create_tender_document = snitch(create_tender_document)
    test_put_tender_document = snitch(put_tender_document)
    test_patch_tender_document = snitch(patch_tender_document)


class AssetDocumentResourceTest(AssetContentWebTest, AssetDocumentResourceTestMixin):
    relative_to = os.path.dirname(__file__)
    forbidden_document_modification_actions_status = 'active'  # status, in which operations with tender documents (adding, updating) are forbidden

    test_create_document_active_tendering_status = snitch(create_document_active_tendering_status)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(AssetDocumentResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
