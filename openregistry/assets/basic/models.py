# -*- coding: utf-8 -*-
from schematics.transforms import blacklist
from schematics.types import StringType
from zope.interface import implementer
from pyramid.security import Allow


from openregistry.api.models import (
    plain_role, listing_role, draft_role, schematics_default_role, schematics_embedded_role
)

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
    view_role, create_role, edit_role, Administrator_role
)


class IBasicAsset(IAsset):
     """ Marker interface for basic assets """


@implementer(IBasicAsset)
class Asset(BaseAsset):

    class Options:
        roles = {
            'draft': edit_role,
            'plain': plain_role,
            'create': create_role,
            'edit': edit_role,
            'edit_pending': blacklist('revisions'), #edit_role,
            'pending': view_role,
            'view': view_role,
            'listing': listing_role,
            'Administrator': Administrator_role,
            'default': schematics_default_role,
        }

    assetType = StringType(default="basic")

    def __acl__(self):
        acl = [
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'edit_asset'),
            (Allow, '{}_{}'.format(self.owner, self.owner_token), 'upload_asset_documents'),
        ]
        return acl

    def __local_roles__(self):
        roles = dict([('{}_{}'.format(self.owner, self.owner_token), 'asset_owner')])
        return roles
