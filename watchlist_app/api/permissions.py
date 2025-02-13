from rest_framework import permissions

class IsAdminOrReadOnly(permissions.IsAdminUser): #only admin can edit rest, everyone can send a get request.

    def has_permission(self, request, view):  #控制全局的存取權限
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

        

class IsReviewUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):  #控制物件層級的權限
        if request.method in permissions.SAFE_METHODS:  #定義了只讀的 HTTP 方法（如 GET, HEAD, 或 OPTIONS）
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff