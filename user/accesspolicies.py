from rest_access_policy import AccessPolicy


class StaffOnlyPost(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": "staff",
            "effect": "allow"
        }
    ]


class StaffOnlyAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update", "destroy"],
        "principal": "staff",
        "effect": "allow"
    }]


class AllAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update", "destroy"],
        "principal": "*",
        "effect": "allow"
    }]


class GetOnlyPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve"],
        "principal": "*",
        "effect": "allow"
    }]
