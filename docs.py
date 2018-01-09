# -*- coding: utf-8 -*-
from uuid import uuid4

from openregistry.api.tests.base import DumpsTestAppwebtest, PrefixedRequestClass
from openregistry.assets.basic.tests.base import BaseAssetWebTest


class AssetResourceTest(BaseAssetWebTest):

    def setUp(self):
        self.app = DumpsTestAppwebtest(
            "config:tests.ini", relative_to=self.relative_to)
        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('broker', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db

    def test_docs_tutorial(self):
        request_path = '/?opt_pretty=1'

        # Exploring basic rules
        #
        with open('docs/source/tutorial/asset-listing.http', 'w') as self.app.file_obj:
            response = self.app.get(request_path)
            self.assertEqual(response.status, '200 OK')
            self.app.file_obj.write("\n")

        with open('docs/source/tutorial/asset-post-attempt.http', 'w') as self.app.file_obj:
            response = self.app.post(request_path, 'data', status=415)
            self.assertEqual(response.status, '415 Unsupported Media Type')


        with open('docs/source/tutorial/asset-post-attempt-json.http', 'w') as self.app.file_obj:
            response = self.app.post(
                request_path, 'data', content_type='application/json', status=422)
            self.assertEqual(response.status, '422 Unprocessable Entity')

        # Creating asset in draft status
        #
        with open('docs/source/tutorial/asset-post-2pc.http', 'w') as self.app.file_obj:
            response = self.app.post_json(request_path, {"data": self.initial_data})
            self.assertEqual(response.status, '201 Created')

        asset_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        # Switch to 'pending'
        #
        with open('docs/source/tutorial/asset-patch-2pc.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')


        with open('docs/source/tutorial/blank-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/pending-first-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')

        # Hack for update_after
        #
        self.app.get(request_path)
        #
        with open('docs/source/tutorial/initial-asset-listing.http', 'w') as self.app.file_obj:
            response = self.app.get(request_path)
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/create-second-asset.http', 'w') as self.app.file_obj:
            response = self.app.post_json(request_path, {"data": self.initial_data})
            self.assertEqual(response.status, '201 Created')


        with open('docs/source/tutorial/pending-second-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/listing-with-some-assets.http', 'w') as self.app.file_obj:
            response = self.app.get(request_path)
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        # Modifying asset
        #
        with open('docs/source/tutorial/patch-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token), {'data':
                {
                    "description": "Земельні ділянки із великими покладами благородних металів"
                }
            })
            self.assertEqual(response.status, '200 OK')

        self.app.get(request_path)
        with open('docs/source/tutorial/asset-listing-after-patch.http', 'w') as self.app.file_obj:
            response = self.app.get(request_path)
            self.assertEqual(response.status, '200 OK')


        with open('docs/source/tutorial/delete-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": "deleted"}})
            self.assertEqual(response.status, '200 OK')

    def test_docs_tutorial_with_concierge(self):
        request_path = '/?opt_pretty=1'

        response = self.app.post_json(request_path, {"data": self.initial_data})
        self.assertEqual(response.status, '201 Created')

        asset_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        response = self.app.patch_json('/{}?acc_token={}'.format(asset_id, owner_token),
                                       {'data': {"status": 'pending'}})
        self.assertEqual(response.status, '200 OK')

        # Switch to Active
        #
        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'verification',
                                                 "relatedLot": uuid4().hex}})
        self.assertEqual(response.status, '200 OK')


        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'active'}})
        self.assertEqual(response.status, '200 OK')


        with open('docs/source/tutorial/attached-to-lot-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'pending',
                                                 "relatedLot": None}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/detached-from-lot-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'verification',
                                                 "relatedLot": uuid4().hex}})
        self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('concierge', ''))

        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'active'}})
        self.assertEqual(response.status, '200 OK')

        # Switch to Complete
        #
        response = self.app.patch_json('/{}'.format(asset_id),
                                       {'data': {"status": 'complete'}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/complete-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')
