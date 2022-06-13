import enrolment
from .serializers import UserSerializer
from rest_framework import status
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from enrolment import serializers

@api_view(['GET'])
def users_list(request,id):
    try:
        userid=User.objects.get(id=id)
        serializer = UserSerializer(userid)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)