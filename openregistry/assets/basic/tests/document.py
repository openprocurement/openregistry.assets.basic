# -*- coding: utf-8 -*-
import unittest

from openregistry.api.tests.blanks.mixins import ResourceDocumentTestMixin
from openregistry.assets.basic.tests.base import (
    AssetContentWebTest
)


class AssetDocumentWithDSResourceTest(AssetContentWebTest, ResourceDocumentTestMixin):
    docservice = True

    # status, in which operations with asset documents (adding, updating) are forbidden
    forbidden_document_modification_actions_status = 'active'


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetDocumentWithDSResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
