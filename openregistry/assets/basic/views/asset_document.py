# -*- coding: utf-8 -*-
from openregistry.api.utils import (
    get_file,
    upload_file,
    update_file_content_type,
    json_view,
    context_unpack,
    APIResource,
)
from openregistry.assets.core.utils import (
    save_asset, opassetsresource, apply_patch,
)

from openregistry.api.validation import (
    validate_file_update,
    validate_file_upload,
    validate_patch_document_data,
)
from openregistry.assets.core.validation import validate_asset_document_update_not_by_author_or_asset_owner

from openregistry.assets.basic.validation import validate_document_operation_in_not_allowed_asset_status


@opassetsresource(name='basic:Asset Documents',
                  collection_path='/assets/{asset_id}/documents',
                  path='/assets/{asset_id}/documents/{document_id}',
                  assetType='basic',
                  description="Asset related binary files (PDFs, etc.)")
class AssetDocumentResource(APIResource):

    @json_view(permission='view_asset')
    def collection_get(self):
        """Asset Documents List"""
        if self.request.params.get('all', ''):
            collection_data = [i.serialize("view") for i in self.context.documents]
        else:
            collection_data = sorted(dict([
                (i.id, i.serialize("view"))
                for i in self.context.documents
            ]).values(), key=lambda i: i['dateModified'])
        return {'data': collection_data}

    @json_view(permission='upload_asset_documents', validators=(validate_file_upload, validate_document_operation_in_not_allowed_asset_status))
    def collection_post(self):
        """Asset Document Upload"""
        document = upload_file(self.request)
        document.author = self.request.authenticated_role
        self.context.documents.append(document)
        if save_asset(self.request):
            self.LOGGER.info('Created asset document {}'.format(document.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_create'}, {'document_id': document.id}))
            self.request.response.status = 201
            document_route = self.request.matched_route.name.replace("collection_", "")
            self.request.response.headers['Location'] = self.request.current_route_url(_route_name=document_route, document_id=document.id, _query={})
            return {'data': document.serialize("view")}

    @json_view(permission='view_asset')
    def get(self):
        """Asset Document Read"""
        if self.request.params.get('download'):
            return get_file(self.request)
        document = self.request.validated['document']
        document_data = document.serialize("view")
        document_data['previousVersions'] = [
            i.serialize("view")
            for i in self.request.validated['documents']
            if i.url != document.url
        ]
        return {'data': document_data}

    @json_view(permission='upload_asset_documents', validators=(validate_file_update, validate_document_operation_in_not_allowed_asset_status,
               validate_asset_document_update_not_by_author_or_asset_owner))
    def put(self):
        """Asset Document Update"""
        document = upload_file(self.request)
        self.request.validated['asset'].documents.append(document)
        if save_asset(self.request):
            self.LOGGER.info('Updated asset document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_put'}))
            return {'data': document.serialize("view")}

    @json_view(content_type="application/json", permission='upload_asset_documents', validators=(validate_patch_document_data,
               validate_document_operation_in_not_allowed_asset_status, validate_asset_document_update_not_by_author_or_asset_owner))
    def patch(self):
        """Asset Document Update"""
        if apply_patch(self.request, src=self.request.context.serialize()):
            update_file_content_type(self.request)
            self.LOGGER.info('Updated asset document {}'.format(self.request.context.id),
                        extra=context_unpack(self.request, {'MESSAGE_ID': 'asset_document_patch'}))
            return {'data': self.request.context.serialize("view")}
