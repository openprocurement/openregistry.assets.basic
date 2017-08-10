# -*- coding: utf-8 -*-
from openregistry.api.utils import raise_operation_error

from openregistry.assets.basic.constants import STATUS_CHANGES


def validate_change_asset_status(request, error_handler, **kwargs):
    """Validate method that check status changes."""
    new_status = request.validated['data'].get("status")
    asset = request.context

    if not new_status or new_status == asset.status:
        return

    statuses = STATUS_CHANGES[asset.status]
    if new_status not in statuses or request.authenticated_role not in statuses.get(new_status, {}):
        raise_operation_error(request, error_handler,
                              'Can\'t update asset in current ({}) status'.format(asset.status))


def validate_asset_status_update_in_terminated_status(request, error_handler, **kwargs):
    asset = request.context
    if asset.status in ['complete', 'deleted']:
        raise_operation_error(request, error_handler, 'Can\'t update asset in current ({}) status'.format(asset.status))