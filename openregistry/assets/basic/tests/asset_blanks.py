# -*- coding: utf-8 -*-
from uuid import uuid4

from openregistry.api.utils import get_now
from openregistry.api.constants import ROUTE_PREFIX

from openregistry.assets.basic.models import Asset


# AssetTest


def simple_add_asset(self):

    u = Asset(self.initial_data)
    u.assetID = "UA-X"

    assert u.id is None
    assert u.rev is None

    u.store(self.db)

    assert u.id is not None
    assert u.rev is not None

    fromdb = self.db.get(u.id)

    assert u.assetID == fromdb['assetID']
    assert u.doc_type == "Asset"

    u.delete_instance(self.db)


def listing(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    offset = get_now().isoformat()

    assets = []

    for _ in range(3):
        offset = get_now().isoformat()
        asset = self.create_asset()
        assets.append(asset)

    ids = ','.join([i['id'] for i in assets])

    for _ in range(10):
        response = self.app.get('/assets')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in assets]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]), set([i['dateModified'] for i in assets]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in assets]))

    for _ in range(10):
        response = self.app.get('/assets?offset={}'.format(offset))
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/assets?limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('prev_page', response.json)
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.get('/assets', params=[('opt_fields', 'status')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status']))
    self.assertIn('opt_fields=status', response.json['next_page']['uri'])

    response = self.app.get('/assets?descending=1')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in assets]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in assets], reverse=True))

    response = self.app.get('/assets?descending=1&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    self.create_asset(extra={"mode": "test"})

    for _ in range(10):
        response = self.app.get('/assets?mode=test')
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/assets?mode=_all_')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 4)


def listing_changes(self):
    response = self.app.get('/assets?feed=changes')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    assets = [self.create_asset() for _ in range(3)]

    ids = ','.join([i['id'] for i in assets])

    for _ in range(10):
        response = self.app.get('/assets?feed=changes')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(','.join([i['id'] for i in response.json['data']]), ids)
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in assets]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]), set([i['dateModified'] for i in assets]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in assets]))

    response = self.app.get('/assets?feed=changes&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('prev_page', response.json)
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.get('/assets?feed=changes', params=[('opt_fields', 'status')])
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified', u'status']))
    self.assertIn('opt_fields=status', response.json['next_page']['uri'])

    response = self.app.get('/assets?feed=changes&descending=1')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in assets]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in assets], reverse=True))

    response = self.app.get('/assets?feed=changes&descending=1&limit=2')
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 2)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get(response.json['next_page']['path'].replace(ROUTE_PREFIX, ''))
    self.assertEqual(response.status, '200 OK')
    self.assertNotIn('descending=1', response.json['prev_page']['uri'])
    self.assertEqual(len(response.json['data']), 0)

    self.create_asset(extra={"mode": "test"})

    for _ in range(10):
        response = self.app.get('/assets?feed=changes&mode=test')
        self.assertEqual(response.status, '200 OK')
        if len(response.json['data']) == 1:
            break
    self.assertEqual(len(response.json['data']), 1)

    response = self.app.get('/assets?feed=changes&mode=_all_')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 4)


def listing_draft(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    assets = [self.create_asset() for _ in range(3)]

    ids = ','.join([i['id'] for i in assets])

    for _ in range(10):
        response = self.app.get('/assets')
        self.assertTrue(ids.startswith(','.join([i['id'] for i in response.json['data']])))
        if len(response.json['data']) == 3:
            break

    self.assertEqual(len(response.json['data']), 3)
    self.assertEqual(set(response.json['data'][0]), set([u'id', u'dateModified']))
    self.assertEqual(set([i['id'] for i in response.json['data']]), set([i['id'] for i in assets]))
    self.assertEqual(set([i['dateModified'] for i in response.json['data']]), set([i['dateModified'] for i in assets]))
    self.assertEqual([i['dateModified'] for i in response.json['data']], sorted([i['dateModified'] for i in assets]))


def create_asset(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/assets', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    asset = response.json['data']

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(set(response.json['data']), set(asset))
    self.assertEqual(response.json['data'], asset)

    response = self.app.post_json('/assets?opt_jsonp=callback', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/javascript')
    self.assertIn('callback({"', response.body)

    response = self.app.post_json('/assets?opt_pretty=1', {"data": self.initial_data})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)

    response = self.app.post_json('/assets', {"data": self.initial_data, "options": {"pretty": True}})
    self.assertEqual(response.status, '201 Created')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "', response.body)


def get_asset(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_asset()

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    response = self.app.get('/assets/{}?opt_jsonp=callback'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/javascript')
    self.assertIn('callback({"data": {"', response.body)

    response = self.app.get('/assets/{}?opt_pretty=1'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertIn('{\n    "data": {\n        "', response.body)


def patch_asset(self):
    data = self.initial_data.copy()
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    asset = self.create_asset()
    owner_token = self.asset_token
    dateModified = asset.pop('dateModified')

    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'title': ' PATCHED' }})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertNotEqual(response.json['data']['dateModified'], dateModified)

    asset = self.create_asset()
    self.set_status('draft')
    owner_token = self.asset_token

    # Move status from Draft to Active
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'active'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Deleted
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Complete
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'complete'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (draft) status")

    # Move status from Draft to Pending
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    # Move status from Pending to Draft
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Pending to Active
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'active'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Complete
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'complete'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Deleted
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'deleted'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'deleted')

    # Move status from Deleted to Draft
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Pending
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'pending'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Active
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'active'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")

    # Move status from Deleted to Complete
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], owner_token), {'data': {'status': 'complete'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def dateModified_asset(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.post_json('/assets', {'data': self.initial_data})
    self.assertEqual(response.status, '201 Created')
    asset = response.json['data']
    token = response.json['access']['token']
    dateModified = asset['dateModified']

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['dateModified'], dateModified)

    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], token), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    self.assertNotEqual(response.json['data']['dateModified'], dateModified)
    asset = response.json['data']
    dateModified = asset['dateModified']

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)
    self.assertEqual(response.json['data']['dateModified'], dateModified)


def asset_not_found(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    response = self.app.get('/assets/some_id', status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'asset_id'}
    ])

    response = self.app.patch_json(
        '/assets/some_id', {'data': {}}, status=404)
    self.assertEqual(response.status, '404 Not Found')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['status'], 'error')
    self.assertEqual(response.json['errors'], [
        {u'description': u'Not Found', u'location': u'url', u'name': u'asset_id'}
    ])

    # put custom document object into database to check asset construction on non-Asset data
    data = {'contract': 'test', '_id': uuid4().hex}
    self.db.save(data)

    response = self.app.get('/assets/{}'.format(data['_id']), status=404)
    self.assertEqual(response.status, '404 Not Found')


def asset_concierge_patch(self):
    asset = self.create_asset()

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    # Move status from Draft to Pending
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], self.asset_token), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    self.app.authorization = ('Basic', ('concierge', ''))

    # Move status from pending to verification
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')


    # Move status from verification to Pending
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')


    # Move status from pending to verification
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')

    # Move status from verification to Active
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'active'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')

    # Move status from Active to Draft
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Active to Deleted
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (active) status")

    # Move status from Active to Pending
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'pending'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'pending')

    # Move status from Pending to Deleted
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")

    # Move status from Pending to Draft
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'draft'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't switch asset to draft status")

    # Move status from Pending to Complete
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'complete'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (pending) status")


    # Move status from pending to verification
    response = self.app.patch_json('/assets/{}?acc_token={}'.format(
        asset['id'], self.asset_token), {'data': {'status': 'verification'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'verification')


    # Move status from verification to active
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'active'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'active')

    # Move status from Active to Complete
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'complete'}})
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data']['status'], 'complete')

    # Move status from Complete to Draft
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Pending
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Active
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")

    # Move status from Complete to Deleted
    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")


def administrator_change_delete_status(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_asset()

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'deleted'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (deleted) status")


def administrator_change_complete_status(self):
    response = self.app.get('/assets')
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(len(response.json['data']), 0)

    self.app.authorization = ('Basic', ('broker', ''))
    asset = self.create_asset()

    response = self.app.get('/assets/{}'.format(asset['id']))
    self.assertEqual(response.status, '200 OK')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['data'], asset)

    self.app.authorization = ('Basic', ('administrator', ''))

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    # XXX TODO Describe actives
    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'active'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'pending'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'verification'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'active'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json(
        '/assets/{}'.format(asset['id']),
        {'data': {'status': 'complete'}}
    )
    self.assertEqual(response.status, '200 OK')

    response = self.app.patch_json('/assets/{}'.format(
        asset['id']), {'data': {'status': 'deleted'}}, status=403)
    self.assertEqual(response.status, '403 Forbidden')
    self.assertEqual(response.content_type, 'application/json')
    self.assertEqual(response.json['errors'][0]['name'], u'data')
    self.assertEqual(response.json['errors'][0]['location'], u'body')
    self.assertEqual(response.json['errors'][0]['description'], u"Can't update asset in current (complete) status")
