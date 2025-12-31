from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from user.models import User

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        user_id = request.query_params.get('user_id') or request.data.get('user_id')

        if not user_id:
            raise PermissionDenied("Se debe especificar user_id.")
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise PermissionDenied("Usuario no encontrado.")
        
        if getattr(user, 'role', '').lower() != 'admin':
            raise PermissionDenied("Este usuario no posee los permisos necesarios.")
        
        return True