# -*- coding: utf-8 -*-


STATUS_CHANGES = {
    "draft": {
        "editing_permissions": ["asset_owner"],
        "next_status": {
            "pending": "asset_owner"
        }
    },
    "pending": {
        "editing_permissions": ["asset_owner", "concierge", "Administrator"],
        "next_status": {
            "deleted": ["asset_owner", "Administrator"],
            "verification": ["concierge", "Administrator"]
        }
    },
    "verification": {
        "editing_permissions":  ["concierge", "Administrator"],
        "next_status": {
            "active": ["concierge", "Administrator"],
            "pending": ["concierge", "Administrator"]
        }
    },
    "active": {
        "editing_permissions": ["concierge", "Administrator"],
        "next_status": {
            "pending": ["concierge", "Administrator"],
            "complete": ["concierge", "Administrator"]
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
