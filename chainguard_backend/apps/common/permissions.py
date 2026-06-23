from rest_framework.permissions import BasePermission

class IsOfficer(BasePermission):
    #Default message:"You do not have permission to perform this action."
    message = "Only officers can perform this action." #Custom message
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=="OFFICER"
    

class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=="SUPERVISOR"
    

class IsSuperVisorOrOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["OFFICER","SUPERVISOR"]
    

class IsStorageClerk(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==["STORAGE_CLERK"]
    

class IsAnlyst(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==["ANALYST"]
    

class IsProfileComplete(BasePermission):
    message = "Please complete your profile before accessing this resource."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile_complete