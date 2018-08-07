# -*- coding: utf-8 -*-
import logging

from pyramid.interfaces import IRequest
from openregistry.assets.core.includeme import IContentConfigurator
from openregistry.assets.core.interfaces import IAssetManager
from openregistry.assets.basic.models import Asset, IBasicAsset
from openregistry.assets.basic.adapters import BasicAssetConfigurator, BasicAssetManagerAdapter
from openregistry.assets.basic.constants import DEFAULT_ASSET_BASIC_TYPE

LOGGER = logging.getLogger(__name__)


def includeme(config, plugin_config=None):
    config.scan("openregistry.assets.basic.views")
    config.scan("openregistry.assets.basic.subscribers")
    config.registry.registerAdapter(BasicAssetConfigurator,
                                    (IBasicAsset, IRequest),
                                    IContentConfigurator)
    config.registry.registerAdapter(BasicAssetManagerAdapter,
                                    (IBasicAsset, ),
                                    IAssetManager)

    asset_types = plugin_config.get('aliases', [])
    if plugin_config.get('use_default', False):
        asset_types.append(DEFAULT_ASSET_BASIC_TYPE)
    for at in asset_types:
        config.add_assetType(Asset, at)

    LOGGER.info("Included openregistry.assets.basic plugin", extra={'MESSAGE_ID': 'included_plugin'})

    # add accreditation level
    config.registry.accreditation['asset'][Asset._internal_type] = plugin_config['accreditation']
