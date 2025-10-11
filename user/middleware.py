import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):

        # Rutas que no requieren token (with and without trailing slash)
        public_paths = [
            '/user/login/',
            '/user/login',
            '/user/registro/',
            '/user/registro',
            '/user/registro-admin/',
            '/user/registro-admin',
        ]
        if request.path in public_paths:
            return None
     
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return JsonResponse({'error': 'Authorization header requerido'}, status=401)

        # Formato: "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return JsonResponse({'error': 'Formato de token inválido'}, status=401)

        token = parts[1]
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except ExpiredSignatureError:
            return JsonResponse({'error': 'Token expirado'}, status=401)
        except InvalidTokenError:
            return JsonResponse({'error': 'Token inválido'}, status=401)

        # Se guarda user_id en el request
        request.user_id = payload.get('user_id')