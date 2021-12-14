from rest_access_policy import AccessPolicy

from account.models import UserProfile


class StaffOnlyPost(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update", "destroy"],
            "principal": "staff",
            "effect": "allow"
        }
    ]


class AuthenticatedGetAccess(AccessPolicy):
    statements = [{
        "action": ["<safe_methods>"],
        "principal": "authenticated",
        "effect": "allow"
    }]


class AuthenticatedAllAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update",
                   "destroy", "create_checkout_session"],
        "principal": "authenticated",
        "effect": "allow"
    }]

class StaffOnlyAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update",
                   "destroy", "fam_est_all_specific_user"],
        "principal": "staff",
        "effect": "allow"
    }]


class AllAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update", "destroy"],
        "principal": "*",
        "effect": "allow"
    }]

class FamFormPostAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "create", "update", "partial_update",
                   "destroy", "create_checkout_session"],
        "principal": "authenticated",
        "effect": "allow",
        "condition": ["has_estimates_remaining"]
    }]
    def has_estimates_remaining(self, request, view, action):
        userProfile = UserProfile.objects.get(user=request.user)
        est_remaining = userProfile.estimates_remaining
        if est_remaining > 0:
            return True
        else:
            return False


class GetOnlyPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve"],
        "principal": "*",
        "effect": "allow"
    }]
