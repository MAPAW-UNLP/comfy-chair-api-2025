import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics, status
from .models import User
from .serializers import UserSerializer, LoginSerializer
from article.models import Article
from reviewer.models import Review, Bid
from django.db.models import OuterRef, Subquery
from chair.models import ReviewAssignment
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import check_password

class UserRegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, role="user")  

class AdminRegisterAPI(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.create(self.request.data, role="admin")  

class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            payload = {
                "user_id": user.id,
                "rol": user.role,
                "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_EXP_DELTA_SECONDS),
                "iat": datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

            return JsonResponse({
                "status": "ok",
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "affiliation": user.affiliation,
                    "role": user.role,
                } 
            }, status=200)

        return JsonResponse(
            {"error": "Email o contraseña incorrecto."},
            status=401
        )

class GetUserIdAPI(APIView):
    def get(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
        
        return JsonResponse({
            'id': usuario.id,
            'full_name': usuario.full_name,
            'email': usuario.email,
            'affiliation': usuario.affiliation,
        }, status=200)
    
# Creado por el Grupo 1 para traer todos los usuarios de la base de datos
# Se requiere para poder seleccionar los autores de un articulo
# No esta protegido por JWT pero deberia estarlo de alguna forma, se deja asi para facilitar el merge
class GetUserListAPI(APIView):
    def get(self, request):
        usuarios = User.objects.all()
        usuarios_data = [
            {
                'id': usuario.id,
                'full_name': usuario.full_name,
                'email': usuario.email,
                'role': usuario.role,
            } for usuario in usuarios
        ]
        return JsonResponse(usuarios_data, safe=False, status=200)

class GetUserFullDataAPI(APIView):
    def get(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        # Subquery para obtener score y opinion si ya existe revisión
        reviews_subquery = Review.objects.filter(
            reviewer=usuario,
            article=OuterRef('article')
        ).values('score', 'opinion')[:1]

        # Artículos donde el usuario es autor
        authored_articles = Article.objects.filter(authors=usuario).select_related('session__conference')

        # Artículos asignados al usuario como revisor
        assigned_reviews = ReviewAssignment.objects.filter(reviewer=usuario).annotate(
            score=Subquery(reviews_subquery.values('score')),
            opinion=Subquery(reviews_subquery.values('opinion'))
        ).select_related('article__session__conference')

        # Conferencias donde es chair general
        conference_chairs = usuario.conferences.all().values('id', 'title')

        # Sesiones donde es chair
        session_chairs = usuario.session.all().select_related('conference').values(
            'id', 'title', 'conference__id', 'conference__title')

        # Estructura jerárquica: conferencia → sesión → roles → artículos
        conferences_data = {}

        # Procesar artículos donde es autor
        for art in authored_articles:
            conf = art.session.conference
            sess = art.session
            conf_entry = conferences_data.setdefault(conf.id, {
                'conference_id': conf.id,
                'conference_name': conf.title,
                'sessions': {}
            })
            sess_entry = conf_entry['sessions'].setdefault(sess.id, {
                'session_id': sess.id,
                'session_name': sess.title,
                'roles': {}
            })
            role_entry = sess_entry['roles'].setdefault('autor', [])
            role_entry.append({
                'id': art.id,
                'title': art.title,
                'status': art.status,
                'type': art.type,
            })

        # Procesar artículos donde es revisor
        for assign in assigned_reviews:
            art = assign.article
            conf = art.session.conference
            sess = art.session
            conf_entry = conferences_data.setdefault(conf.id, {
                'conference_id': conf.id,
                'conference_name': conf.title,
                'sessions': {}
            })
            sess_entry = conf_entry['sessions'].setdefault(sess.id, {
                'session_id': sess.id,
                'session_name': sess.title,
                'roles': {}
            })
            role_entry = sess_entry['roles'].setdefault('revisor', [])
            role_entry.append({
                'id': art.id,
                'title': art.title,
                'score': assign.score,
                'opinion': assign.opinion,
            })

        # Convertir dicts a listas
        conferences_list = []
        for conf_data in conferences_data.values():
            sessions_list = []
            for sess_data in conf_data['sessions'].values():
                roles_list = []
                for role, arts in sess_data['roles'].items():
                    roles_list.append({'role': role, 'articles': arts})
                sess_data['roles'] = roles_list
                sessions_list.append(sess_data)
            conf_data['sessions'] = sessions_list
            conferences_list.append(conf_data)

        # Estructura final del usuario
        data = {
            'user': {
                'id': usuario.id,
                'full_name': usuario.full_name,
                'email': usuario.email,
                'affiliation': usuario.affiliation,
                'role': usuario.role,
                'is_conference_chair': conference_chairs.exists(),
                'conference_chair_of': list(conference_chairs),
                'is_session_chair': session_chairs.exists(),
                'session_chair_of': list(session_chairs),
            },
            'conferences': conferences_list
        }

        return JsonResponse(data, safe=False, status=200)

# Lo agregamos desde el grupo 3 para obtener usuarios que sean solo user, se ordena alfabeticamente
# Por ahora se evita usar JWT, se agrega mas adelante
class GetUsersNoAdminAPI(APIView):
    def get(self, request):
        users = User.objects.filter(role="user").order_by('full_name')
        users_data = [
            {
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
            } for user in users
        ]
        return JsonResponse(users_data, safe=False, status=200)


class UpdateUserDataAPI(APIView):
    def put(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        data = request.data
        full_name = data.get('full_name')
        affiliation = data.get('affiliation')
        email = data.get('email')

        # Validar email duplicado si es distinto
        if email and email != user.email:
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'El email ya está registrado por otro usuario.'}, status=400)
            user.email = email

        # Actualizar campos básicos
        if full_name:
            user.full_name = full_name
        if affiliation:
            user.affiliation = affiliation

        user.save()

        return JsonResponse({
            'message': 'Datos actualizados correctamente.',
            'user': {
                'id': user.id,
                'full_name': user.full_name,
                'affiliation': user.affiliation,
                'email': user.email,
            }
        }, status=200)


class UpdateUserPasswordAPI(APIView):
    def put(self, request):
        user_id = getattr(request, 'user_id', None)
        if not user_id:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        data = request.data
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        # Validaciones 
        if not all([current_password, new_password, confirm_password]):
            return JsonResponse({'error': 'Todos los campos son obligatorios.'}, status=400)

        if not user.check_password(current_password):
            return JsonResponse({'error': 'La contraseña actual es incorrecta.'}, status=400)

        if new_password != confirm_password:
            return JsonResponse({'error': 'Las contraseñas nuevas no coinciden.'}, status=400)

        if current_password == new_password:
            return JsonResponse({'error': 'La nueva contraseña no puede ser igual a la actual.'}, status=400)

        # Actualizar contraseña
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Contraseña actualizada correctamente.'}, status=200)
