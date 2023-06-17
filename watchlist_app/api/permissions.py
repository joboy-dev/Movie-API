from rest_framework import permissions

class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        # check if request is a GET method or if the user has admin permission
        if request.method in permissions.SAFE_METHODS:
            # check permissions for read request ie GET request

            # allow anyone to read
            return True
        else:
            # check permissions for write request ie POST, PUT, PATCH requests

            # this returns true if current user is also a staff user 
            return bool(request.user and request.user.is_staff)


# permission to allow only owners of a review to edit the review
class ReviewUserOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # check permissions for read request ie GET request

            # allow everyone to read the review
            return True
        else:
            # check permissions for write request ie POST, PUT, PATCH requests

            # this returns true if review owner is the same as current logged in user or if the loggedn in user is a staff account
            return obj.review_user == request.user or request.user.is_staff
        