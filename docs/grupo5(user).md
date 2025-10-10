Documentación grupo5 usuarios (users)

Este módulo se encarga de la gestión de usuarios en la aplicación, incluyendo el registro, autenticación y recuperación de información de usuarios. Implementa autenticación JWT y soporte para roles de usuario (user y admin).


1) Modelos

-User

full_name (CharField): Nombre completo del usuario.

affiliation (CharField): Afiliación del usuario.

email (EmailField): Correo electrónico único del usuario. Se utiliza como identificador (USERNAME_FIELD).

role (CharField, choices=["user", "admin"]): Rol del usuario.

deleted (BooleanField): Indica si el usuario está eliminado lógicamente.


2) Serializers

-UsuarioSerializer

Serializa los datos del usuario (id, full_name, affiliation, email, password).
La contraseña se guarda encriptada usando make_password.
Permite asignar un rol automáticamente desde la vista usando el parámetro role.
password es write-only y no se retorna en las respuestas.


-LoginSerializer

Valida el correo y la contraseña del usuario.
Devuelve el objeto user y un token si la autenticación es exitosa.
Lanza un error si los datos son incorrectos.


3) API Endpoints

-Registro de usuario

POST /user/registro/

Registra un usuario con rol user.
Parámetros: full_name, affiliation, email, password.


-Registro de administrador

POST /user/registro-admin/

Registra un usuario con rol admin.
Parámetros: full_name, affiliation, email, password.


-Login

POST /user/login/

Autentica un usuario y retorna el usuario y un token JWT.
El JWT incluye user_id y role en su payload.
Parámetros: email, password.


-Obtener información del usuario actual

GET /user/getUsuario/

Requiere token JWT válido en el header Authorization: Bearer <token>.
Retorna los datos del usuario autenticado.


4) Middleware

-JWTAuthenticationMiddleware

Intercepta todas las peticiones y valida el JWT en el header Authorization.

Rutas públicas: /users/login/, /users/registro/, /users/registro-admin/.

Valida formato y expiración del token.
Agrega request.user_id si el token es válido.
Devuelve error 401 si el token es inválido, faltante o expirado.


Posibles errores de JWT

"error": "Authorization header requerido": Este error ocurre cuando no se envió el token en el header Authorization. Todo request a un endpoint protegido debe incluir el header Authorization.

"error": "Formato de token inválido": El token enviado no tiene el formato correcto. El formato esperado es: Authorization: Bearer token

"error": "Token expirado": Indica que el token JWT ha caducado. En este caso, el usuario debe volver a iniciar sesión para obtener un nuevo token válido.

"error": "Token inválido": Significa que el token ha sido modificado o no es válido. Puede suceder si se altera el token o si se usa un token de otro usuario.

Nota sobre JWT y middleware:
Si luego del merge se presentan problemas con JWT para acceder a los endpoints (por ejemplo, alguno de los errores mencionados anteriormente), se puede comentar temporalmente la línea 'users.middleware.JWTAuthenticationMiddleware' en la configuración de MIDDLEWARE del proyecto (comfy_chair/settings.py). Esto hará que el middleware no se ejecute y permitirá acceder a las rutas.
