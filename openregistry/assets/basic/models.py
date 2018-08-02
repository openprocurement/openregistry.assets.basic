# -*- coding: utf-8 -*-
from schematics.types import StringType
from schematics.types.compound import ModelType, ListType
from zope.interface import implementer


from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
    Classification,
    koatuu_validator,
)


class IBasicAsset(IAsset):
    """ Marker interface for basic assets """


class AssetAdditionalClassification(Classification):
    id_validators = Classification.id_validators + (koatuu_validator,)


@implementer(IBasicAsset)
class Asset(BaseAsset):
    _internal_type = 'basic'
    assetType = StringType(default="basic")
    additionalClassifications = ListType(ModelType(AssetAdditionalClassification), default=list())
