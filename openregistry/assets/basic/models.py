# -*- coding: utf-8 -*-
from schematics.types import StringType
from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
)


class IBasicAsset(IAsset):
    """ Marker interface for basic assets """


@implementer(IBasicAsset)
class Asset(BaseAsset):
    assetType = StringType(default="basic")
