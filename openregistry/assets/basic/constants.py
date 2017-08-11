# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "pending": "asset_owner"
    },
    "pending": {
        "deleted": "asset_owner",
        "active": "bot1"
    },
    "deleted": {

    },
    "active": {
        "pending": "bot1",
        "complete": "bot1"
    },
    "complete": {

    }
}
