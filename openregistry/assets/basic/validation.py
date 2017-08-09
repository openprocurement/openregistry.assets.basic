# -*- coding: utf-8 -*-
from openregistry.api.validation import validate_json_data
from openregistry.api.utils import raise_operation_error

from openregistry.assets.basic.constants import STATUS_CHANGES


def validate_change_asset_status(request, error_handler, **kwargs):
    '''
        Validate method that check status changes.
    '''
    data = validate_json_data(request)
    asset = request.context
    for status in STATUS_CHANGES:
        if asset.status == status:
            new_status = data.get('status', False)
            auth_role = request.authenticated_role
            if new_status and new_status not in STATUS_CHANGES[status].keys() and auth_role != 'Administrator':
                raise_operation_error(request, error_handler,
                                      'Can\'t update asset in current ({}) status'.format(asset.status))
            elif new_status and auth_role != 'Administrator' and auth_role != STATUS_CHANGES[status].get(new_status, ''):
                raise_operation_error(request, error_handler,
                                      'Can\'t update asset in current ({}) status'.format(asset.status))
            request.validated['data'] = {'status': new_status}
            break


def validate_asset_status_update_in_terminated_status(request, error_handler, **kwargs):
    asset = request.context
    if request.authenticated_role == 'Administrator' and asset.status in ['complete', 'deleted']:
        raise_operation_error(request, error_handler, 'Can\'t update asset in current ({}) status'.format(asset.status))