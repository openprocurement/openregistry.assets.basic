# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.assets.core.constants import DOCUMENT_TYPES
from openregistry.assets.core.tests.base import test_document_data
from openregistry.assets.core.tests.blanks.mixins import ResourceDocumentTestMixin

from openregistry.assets.basic.tests.base import (
    AssetContentWebTest
)


class AssetDocumentWithDSResourceTest(AssetContentWebTest, ResourceDocumentTestMixin):
    docservice = True
    document_types = DOCUMENT_TYPES

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'

    def setUp(self):
        super(AssetDocumentWithDSResourceTest, self).setUp()
        self.initial_document_data = deepcopy(test_document_data)
        self.initial_document_data['url'] = self.generate_docservice_url()


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
