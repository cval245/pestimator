from rest_access_policy import AccessPolicy


class AllGetStaffOnlyPost(AccessPolicy):
    statements = [
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["create", "update", "partial_update", "destroy",
                       "post_lawfirm_image",
                       "post_article_image_image_post", "post_article_image"],
            "principal": "staff",
            "effect": "allow"
        }
    ]


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
        # "condition": ["has_estimates_remaining"]
    }]


class GetOnlyPolicy(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "get_open_estimates", "fam_est_detail_guest",
                   "get_free_pdf_report_fam_est_detail", "get_free_xls_report_fam_est_detail"],
        "principal": "*",
        "effect": "allow"
    }]


class LawFirmPostAndGetAccess(AccessPolicy):
    statements = [{
        "action": ["list", "retrieve", "update", "partial_update",
                   "destroy", "create_checkout_session"],
        "principal": "authenticated",
        "effect": "allow",
        "condition": ["has_lawfirm_submit_data_access"]
    }]

    def has_lawfirm_submit_data_access(self, request, view, action, field):
        return request.user.lawfirm_submit_data_access
