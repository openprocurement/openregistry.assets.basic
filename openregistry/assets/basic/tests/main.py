# -*- coding: utf-8 -*-

import unittest

from openregistry.assets.basic.tests import asset, document


def suite():
    tests = unittest.TestSuite()
    tests.addTest(asset.suite())
    tests.addTest(document.suite())
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
