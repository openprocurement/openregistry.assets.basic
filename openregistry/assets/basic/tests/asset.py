# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy

from openregistry.api.tests.blanks.mixins import ResourceTestMixin
from openregistry.api.tests.blanks.json_data import test_asset_basic_data, test_asset_basic_data_with_schema
from openregistry.assets.core.tests.blanks.mixins import AssetResourceTestMixin

from openregistry.assets.basic.models import Asset as AssetBasic
from openregistry.assets.basic.tests.base import BaseAssetWebTest


class AssetBasicResourceTest(BaseAssetWebTest, ResourceTestMixin, AssetResourceTestMixin):
    asset_model = AssetBasic
    initial_data = test_asset_basic_data
    initial_status = 'pending'

    def test_create_compount_with_item_schemas(self):
        response = self.app.post_json('/?opt_pretty=1', {'data': test_asset_basic_data_with_schema})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        response = response.json['data']
        self.assertEqual(response['title'], test_asset_basic_data_with_schema['title'])
        self.assertEqual(response['assetType'], test_asset_basic_data_with_schema['assetType'])
        self.assertEqual(response['assetCustodian'], test_asset_basic_data_with_schema['assetCustodian'])
        self.assertEqual(response['classification'], test_asset_basic_data_with_schema['classification'])
        self.assertEqual(response['unit'], test_asset_basic_data_with_schema['unit'])
        self.assertEqual(response['quantity'], test_asset_basic_data_with_schema['quantity'])
        self.assertEqual(response['address'], test_asset_basic_data_with_schema['address'])
        self.assertEqual(response['value']['amount'], test_asset_basic_data_with_schema['value']['amount'])
        self.assertEqual(response['value']['currency'], test_asset_basic_data_with_schema['value']['currency'])
        self.assertEqual(response['schema_properties']['properties'], test_asset_basic_data_with_schema['schema_properties']['properties'])
        self.assertEqual(response['schema_properties']['code'][0:2], test_asset_basic_data_with_schema['schema_properties']['code'][:2])

    def test_bad_item_schemas_code(self):
        bad_initial_data = deepcopy(test_asset_basic_data_with_schema)
        bad_initial_data['classification']['id'] = "42124210-6"
        response = self.app.post_json('/', {'data': bad_initial_data},status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'], [{u'description': [u'classification id mismatch with schema_properties code'], u'location': u'body', u'name': u'schema_properties'}])

    def test_delete_item_schema(self):
        response = self.app.post_json('/', {'data': test_asset_basic_data_with_schema})
        self.assertEqual(response.status, '201 Created')
        resource = response.json['data']
        self.resource_token = response.json['access']['token']
        self.access_header = {'X-Access-Token': str(response.json['access']['token'])}
        self.resource_id = resource['id']
        status = resource['status']

        response = self.app.patch_json('/{}?access_token={}'.format(
                                self.resource_id, self.resource_token),
                                headers=self.access_header,
                                params={'data': {'schema_properties': None}})
        #TODO delete schema proderties
        # self.assertEqual(response.json['data']['schema_properties'], None)


def suite():
    tests = unittest.TestSuite()
    tests.addTest(unittest.makeSuite(AssetBasicResourceTest))
    return tests


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
