# -*- coding: utf-8 -*-
import os
from copy import deepcopy

from openregistry.assets.core.tests.base import (
    BaseAssetWebTest as BaseAWT
)


test_organization = {
    "name": u"Державне управління справами",
    "identifier": {
        "scheme": u"UA-EDR",
        "id": u"00037256",
        "uri": u"http://www.dus.gov.ua/"
    },
    "address": {
        "countryName": u"Україна",
        "postalCode": u"01220",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова, 11, корпус 1"
    },
    "contactPoint": {
        "name": u"Державне управління справами",
        "telephone": u"0440000000"
    }
}

test_assetCustodian = test_organization.copy()

test_asset_data = {
    "title": u"Земля для космодрому",
    "assetType": "basic",
    "assetCustodian": test_assetCustodian,
    "classification": {
        "scheme": u"CPV",
        "id": u"37452200-3",
        "description": u"Земельні ділянки"
    },
    "unit": {
        "name": u"item",
        "code": u"44617100-9"
    },
    "quantity": 5,
    "address": {
        "countryName": u"Україна",
        "postalCode": "79000",
        "region": u"м. Київ",
        "locality": u"м. Київ",
        "streetAddress": u"вул. Банкова 1"
    },
    "value": {
        "amount": 100,
        "currency": u"UAH"
    },
}


class BaseAssetWebTest(BaseAWT):
    initial_auth = ('Basic', ('broker', ''))
    relative_to = os.path.dirname(__file__)

    def setUp(self):
        self.initial_data = deepcopy(test_asset_data)
        super(BaseAssetWebTest, self).setUp()


class AssetContentWebTest(BaseAssetWebTest):
    init = True
    initial_status = 'pending'
