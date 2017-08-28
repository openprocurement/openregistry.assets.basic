# -*- coding: utf-8 -*-
from pyramid.events import subscriber
from openregistry.assets.core.events import AssetInitializeEvent
from openregistry.api.utils import get_now


@subscriber(AssetInitializeEvent, assetType="basic")
def tender_init_handler(event):
    """ initialization handler for basic assets """
    event.asset.date = get_now()
