# -*- coding: utf-8 -*-
from openregistry.assets.core.views.mixins import AssetResource
from openregistry.assets.core.utils import opassetsresource


@opassetsresource(name='basic:Asset',
                  path='/assets/{asset_id}',
                  assetType='basic',
                  description="Open Contracting compatible data exchange format.")
class AssetBasicResource(AssetResource):
    pass
