from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from conference_session.models import Session
from rest_framework.views import APIView

class LockSelection(APIView):
    def post(self, request, pk):
        session = get_object_or_404(Session, pk=pk)

        if session.locked_selection:
            return Response(
                {"detail": "Selection already locked"},
                status=400
            )

        # Obtener type_selection desde el body
        type_selection = request.data.get("type_selection")

        if not type_selection:
            return Response(
                {"detail": "You must provide type_selection"},
                status=400
            )

        # Validación opcional: verificar que sea uno de los valores permitidos
        if type_selection not in dict(Session.TYPE_SELECTION_CHOICES):
            return Response(
                {"detail": "Invalid type_selection value"},
                status=400
            )

        # Guardar el tipo y bloquearlo
        session.type_selection = type_selection
        session.locked_selection = True
        session.save()

        return Response(
            {"detail": "Selection locked successfully",
             "locked_type": type_selection},
            status=200
        )
