# -*- coding: utf-8 -*-
from schematics.types import StringType, ValidationError
from schematics.types.compound import ModelType, ListType
from zope.interface import implementer

from openregistry.assets.core.models import (
    IAsset, Asset as BaseAsset,
    AssetAdditionalClassification
)


class IBasicAsset(IAsset):
    """ Marker interface for basic assets """


@implementer(IBasicAsset)
class Asset(BaseAsset):
    _internal_type = 'basic'
    assetType = StringType(default="basic")
    additionalClassifications = ListType(ModelType(AssetAdditionalClassification), default=list())

    def validate_relatedLot(self, data, lot):
        if data['status'] == 'active' and not lot:
            raise ValidationError(u'This field is required.')
