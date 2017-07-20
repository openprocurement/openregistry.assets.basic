# -*- coding: utf-8 -*-

import unittest

from openregistry.assets.basic.tests import asset


def suite():
    suite = unittest.TestSuite()
    suite.addTest(asset.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
