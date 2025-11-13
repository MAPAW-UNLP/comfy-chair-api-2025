# Aspectos del Back Desarrollados por el Grupo 1

    El grupo 1 se encargó de desarrollar la app "article" que maneja de la lectura, alta, baja y modificación de articulos.

# ---------- Models (models.py) ----------

    [Article]
    Campos Propios:
        * title = titulo del artículo.
        * main_file = ruta donde se encuentra el archivo que contiene el articulo.
        * status = estado del articulo (reception, bidding, assignment, review, selection, accepted o rejected).
        * type = tipo de articulo (regular o poster).
        * abstract = descripción corta del articulo de hasta 300 caracteres.
        * source_file = ruta donde se encuentra el archivo que contiene las fuentes (solo se guarda cuando el articulo es de tipo poster).

    Campos de Relaciones:
        * authors = contiene un arreglo con todos los id de usuarios de la app que son       autores del articulo.
        * corresponding_author = contiene el id de usuario de la app que es el autor de notificación designado.
        * session = contiene el id de la sesion a la que pertenece el articulo.

    [ArticleDeletionRequest] -> Cuando el articulo ya fue aceptado y el autor solicita la baja del mismo.
    Campos Propios:
        * description = motivo de la solicitud de eliminación (hasta 300 caracteres).
        * status = estado de la solicitud (pending, accepted o rejected).
        * created_at = fecha y hora de creación de la solicitud.
        * updated_at = fecha y hora de última actualización de la solicitud.

    Campos de Relaciones:
        * article = contiene el id del artículo que se solicita eliminar.

# ---------- Serializer (serializers.py) ----------

    [ArticleSerializer]
    Lectura:
        * Devuelve todos los campos del modelo "Article".
        * Importa los serizalizers de "user" y "conference_session" para mostrar los datos pertenecienteas a otras tablas.

    Escritura:
        * Permite escribir todos los campos del modelo "Article".
        * Importa los serizalizers de "user" y "conference_session" para mostrar los datos pertenecienteas a otras tablas.

    [ArticleDeletionRequestSerializer]
    Lectura:
        * Devuelve todos los campos del modelo "ArticleDeletionRequest".
        * Importa el serializer de "article" para mostrar los datos del artículo asociado.

    Escritura:
        * Permite escribir los campos article_id, description y status del modelo "ArticleDeletionRequest".
        * article_id es write-only y permite establecer la relación con el artículo.

# ---------- Endpoints (views.py) ----------

    Endpoints Article:
    POST    /api/article/
    PUT     /api/article/{articleId}/
    PATCH   /api/article/{articleId}/
    DELETE  /api/article/{articleId}/
    GET     /api/article/{articleId}/
    GET     /api/article/{articleId}/download_main/
    GET     /api/article/{articleId}/download_source/
    GET     /api/article/getArticlesByConferenceId/{conferenceId}/
    GET     /api/article/getArticlesBySessionId/{sessionId}/

    Endpoints ArticleDeletionRequest:
    POST    /api/article-deletion-request/
    GET     /api/article-deletion-request/
    GET     /api/article-deletion-request/{deletionRequestId}/
    PUT     /api/article-deletion-request/{deletionRequestId}/
    PATCH   /api/article-deletion-request/{deletionRequestId}/
    DELETE  /api/article-deletion-request/{deletionRequestId}/
    PATCH   /api/article-deletion-request/{deletionRequestId}/accept/
    PATCH   /api/article-deletion-request/{deletionRequestId}/reject/
