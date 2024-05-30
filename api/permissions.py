from rest_framework.permissions import BasePermission

import strings


class CanUpdateRequest(BasePermission):
    """
    This permission will ensure that the request status will be 
    updated by the user who received the request.

    The sender of the request cannot update the request status
    """
    message = strings.REQUEST_UPDATE_ERROR

    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.to_user_id
