# -*- coding: utf-8 -*-

STATUS_CHANGES = {
    "draft": {
        "pending": "asset_owner"
    },
    "pending": {
        "deleted": ["asset_owner", "Administrator"],
        "active": ["bot", "Administrator"],
        "draft": ["Administrator"]
    },
    "deleted": {

    },
    "active": {
        "pending": ["bot", "Administrator"],
        "complete": ["bot", "Administrator"]
    },
    "complete": {

    }
}
