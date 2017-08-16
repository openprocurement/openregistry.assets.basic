# -*- coding: utf-8 -*-
import json
import os
from datetime import timedelta, datetime
from time import sleep
from uuid import uuid4

from openregistry.api.utils import get_now
from openregistry.api.tests.base import PrefixedRequestClass
from openregistry.assets.basic.tests.base import test_asset_data, BaseAssetWebTest
from webtest import TestApp

test_asset_data = test_asset_data.copy()


class DumpsTestAppwebtest(TestApp):
    def do_request(self, req, status=None, expect_errors=None):
        req.headers.environ["HTTP_HOST"] = "lb.api-sandbox.registry.ea.openprocurement.net"
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            self.file_obj.write(req.as_bytes(True))
            self.file_obj.write("\n")
            if req.body:
                try:
                    self.file_obj.write(
                        '\n' + json.dumps(json.loads(req.body), indent=2, ensure_ascii=False).encode('utf8'))
                    self.file_obj.write("\n")
                except:
                    pass
            self.file_obj.write("\n")
        resp = super(DumpsTestAppwebtest, self).do_request(req, status=status, expect_errors=expect_errors)
        if hasattr(self, 'file_obj') and not self.file_obj.closed:
            headers = [(n.title(), v)
                       for n, v in resp.headerlist
                       if n.lower() != 'content-length']
            headers.sort()
            self.file_obj.write(str('\n%s\n%s\n') % (
                resp.status,
                str('\n').join([str('%s: %s') % (n, v) for n, v in headers]),
            ))

            if resp.testbody:
                try:
                    self.file_obj.write('\n' + json.dumps(json.loads(resp.testbody), indent=2, ensure_ascii=False).encode('utf8'))
                except:
                    pass
            self.file_obj.write("\n\n")
        return resp


class AssetResourceTest(BaseAssetWebTest):
    initial_data = test_asset_data

    def setUp(self):
        self.app = DumpsTestAppwebtest(
            "config:tests.ini", relative_to=self.relative_to)
        self.app.RequestClass = PrefixedRequestClass
        self.app.authorization = ('Basic', ('broker', ''))
        self.couchdb_server = self.app.app.registry.couchdb_server
        self.db = self.app.app.registry.db

    def test_docs_tutorial(self):
        request_path = '/assets?opt_pretty=1'

        # Exploring basic rules
        #
        self.app.authorization = ('Basic', ('broker', ''))

        with open('docs/source/tutorial/asset-listing.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets')
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
        data = self.initial_data.copy()
        data['status'] = 'draft'

        with open('docs/source/tutorial/asset-post-2pc.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/assets?opt_pretty=1', {"data": data})
            self.assertEqual(response.status, '201 Created')

        asset_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        # switch to 'pending'

        with open('docs/source/tutorial/asset-patch-2pc.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')


        with open('docs/source/tutorial/blank-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/pending-first-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')

        # Hack for update_after
        self.app.get('/assets')
        #
        with open('docs/source/tutorial/initial-asset-listing.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets')
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/create-second-asset.http', 'w') as self.app.file_obj:
            response = self.app.post_json(
                '/assets?opt_pretty=1', {"data": test_asset_data})
            self.assertEqual(response.status, '201 Created')


        with open('docs/source/tutorial/pending-second-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": 'pending'}})
            self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/listing-with-some-assets.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets')
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('broker', ''))

        # Modifying asset
        #

        with open('docs/source/tutorial/patch-asset.http', 'w') as self.app.file_obj:
            response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token), {'data':
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
            response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                           {'data': {"status": "deleted"}})
            self.assertEqual(response.status, '200 OK')

    def test_docs_tutorial_with_bot(self):
        request_path = '/assets?opt_pretty=1'

        response = self.app.post_json(
            '/assets?opt_pretty=1', {"data": self.initial_data})
        self.assertEqual(response.status, '201 Created')

        asset_id = response.json['data']['id']
        owner_token = response.json['access']['token']

        response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                       {'data': {"status": 'pending'}})
        self.assertEqual(response.status, '200 OK')

        # Switch to Verification
        #

        self.app.authorization = ('Basic', ('bot', ''))

        response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                       {'data': {"status": 'verification',
                                                 "relatedLot": uuid4().hex}})
        self.assertEqual(response.status, '200 OK')


        response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                       {'data': {"status": 'active'}})
        self.assertEqual(response.status, '200 OK')

        # Switch to Active
        #

        with open('docs/source/tutorial/attached-to-lot-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('bot', ''))

        response = self.app.patch_json('/assets/{}'.format(asset_id),
                                       {'data': {"status": 'pending',
                                                 "relatedLot": None}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/detached-from-lot-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('bot', ''))

        response = self.app.patch_json('/assets/{}?acc_token={}'.format(asset_id, owner_token),
                                       {'data': {"status": 'verification',
                                                 "relatedLot": uuid4().hex}})
        self.assertEqual(response.status, '200 OK')

        self.app.authorization = ('Basic', ('bot', ''))

        response = self.app.patch_json('/assets/{}'.format(asset_id),
                                       {'data': {"status": 'active'}})
        self.assertEqual(response.status, '200 OK')

        # Switch to Complete
        #

        response = self.app.patch_json('/assets/{}'.format(asset_id),
                                       {'data': {"status": 'complete'}})
        self.assertEqual(response.status, '200 OK')

        with open('docs/source/tutorial/complete-asset-view.http', 'w') as self.app.file_obj:
            response = self.app.get('/assets/{}'.format(asset_id))
            self.assertEqual(response.status, '200 OK')
