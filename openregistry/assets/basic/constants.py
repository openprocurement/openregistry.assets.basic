# -*- coding: utf-8 -*-


STATUS_CHANGES = {
    "draft": {
        "editing_permissions": ["asset_owner"],
        "next_status": {
            "pending": "asset_owner"
        }
    },
    "pending": {
        "editing_permissions": ["asset_owner", "bot", "Administrator"],
        "next_status": {
            "deleted": ["asset_owner", "Administrator"],
            "verification": ["bot", "Administrator"]
        }
    },
    "verification": {
        "editing_permissions":  ["bot", "Administrator"],
        "next_status": {
            "active": ["bot", "Administrator"],
            "pending": ["bot", "Administrator"]
        }
    },
    "active": {
        "editing_permissions": ["bot", "Administrator"],
        "next_status": {
            "pending": ["bot", "Administrator"],
            "complete": ["bot", "Administrator"]
        }
    },
    "deleted": {
        "editing_permissions": [],
        "next_status": {}
    },
    "complete": {
        "editing_permissions": [],
        "next_status": {}
    }
}
