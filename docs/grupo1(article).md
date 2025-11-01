### App "article" by Grupo 1

Este módulo se encarga de la gestión de articulos en la aplicación. Permite el alta, baja y modificación de articulos.
También permite guardar los archivos, tanto de los articulos como de las fuentes, en la ruta "media/" en la carpeta root del servidor.

1) Modelo Article

# Campos Propios
- title = titulo del artículo
- main_file = ruta donde se encuentra el archivo que contiene el articulo
- status = estado del articulo (reception, bidding, assignment, review, selection, accepted o rejected)
- type = tipo de articulo (regular o poster)
- abstract = descripción corta del articulo de hasta 300 caracteres
- source_file = ruta donde se encuentra el archivo que contiene las fuentes (solo se guarda cuando el articulo es de tipo poster)

# Campos de Relaciones
- authors = contiene un arreglo con todos los id de usuarios de la app que son autores del articulo
- corresponding_author = contiene el id de usuario de la app que es el autor de notificación designado
- session = contiene el id de la sesion a la que pertenece el articulo

2) Serializers

# Usamos un serializer llamado "ArticleSerializer"

- Para escritura -> usamos el serializer propio
- Para lectura -> ademas importamos serializers de "user" y "conference_session" en modo solo lectura para no permitir alterar campos

3) API Endpoints

# Usamos los endpoins provistos por la api default de Django

- /api/article/ -> Usado para GET de todos los articulos y POST de un articulo
- /api/article/article_id -> Usado para GET de un articulo específico y PUT de un articulo específico