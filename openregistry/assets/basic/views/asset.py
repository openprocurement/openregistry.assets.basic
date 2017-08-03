# -*- coding: utf-8 -*-
from openregistry.api.utils import (
    json_view,
    context_unpack,
    APIResource
)

from openregistry.assets.core.utils import (
    save_asset, opassetsresource, apply_patch
)

from openregistry.assets.core.validation import (
    validate_patch_asset_data,
    validate_asset_status_update_in_terminated_status
)
from openregistry.assets.basic.validation import (
    validate_change_asset_status
)


patch_asset_validators = (validate_asset_status_update_in_terminated_status,
                          validate_change_asset_status,
                          validate_patch_asset_data)


@opassetsresource(name='basic:Asset',
                  path='/assets/{asset_id}',
                  assetType='basic',
                  description="Open Contracting compatible data exchange format.")
class AssetResource(APIResource):

    @json_view(permission='view_asset')
    def get(self):
        asset_data = self.context.serialize(self.context.status)
        return {'data': asset_data}

    @json_view(content_type="application/json",
               validators=patch_asset_validators,
               permission='edit_asset')
    def patch(self):
        asset = self.context
        apply_patch(self.request, src=self.request.validated['asset_src'])
        self.LOGGER.info(
            'Updated asset {}'.format(asset.id),
            extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_patch'})
        )
        return {'data': asset.serialize(asset.status)}
