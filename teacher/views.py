from django.shortcuts import get_object_or_404
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView, Response

from .models import Aula, Professor
from .serializers import (AulaSerializer, CadastrarAulaSerializer,
                          ProfessorSerializer)


class ProfessorAPIView(APIView):
    def get(self, request, format=None):
        professores = Professor.objects.all()
        serializer = ProfessorSerializer(professores, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class CadastrarAulaAPIView(APIView):
    def post(self, request, id, format=None):
        professor = get_object_or_404(Professor, id=id)
        serializer = CadastrarAulaSerializer(data=request.data)

        if serializer.is_valid():
            aula = Aula(
                nome=serializer.validated_data['nome'],
                email=serializer.validated_data['email'],
                professor=professor
            )
            aula.save()
            aula_serializer = AulaSerializer(aula, many=False)
            return Response(aula_serializer.data, status=HTTP_201_CREATED)

        return Response(
            {
                "message": "Houveram erros de validação",
                "errors": serializer.errors
            },
            status=HTTP_400_BAD_REQUEST
        )
