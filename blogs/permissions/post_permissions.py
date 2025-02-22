# blog/permissions/post_permissions.py

from rest_framework import permissions

class IsPostCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Only allow updates if the user is authenticated and is the post's creator.
        if request.user and request.user.is_authenticated:
            return obj.author.user == request.user
        return False