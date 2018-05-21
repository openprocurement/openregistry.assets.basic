# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT,
    test_asset_basic_data
)


class BaseAssetWebTest(BaseAWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)

    def setUp(self):
        self.initial_data = deepcopy(test_asset_basic_data)
        super(BaseAssetWebTest, self).setUp()


class AssetContentWebTest(BaseAssetWebTest):
    init = True
    initial_status = 'pending'

