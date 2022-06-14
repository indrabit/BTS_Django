import enrolment
from .serializers import UserSerializer
from rest_framework import status
from datetime import datetime

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from enrolment import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny,IsAuthenticated

@api_view(['GET'])
def users_list(request,id):
    try:
        userid=User.objects.get(id=id)
        serializer = UserSerializer(userid)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def handleUpdate(request, id):
    
    if request.method == "POST":
        email = str(request.data.get('email'))
        firstname = str(request.data.get('first_name'))
        lastname = str(request.data.get('last_name'))
        mobile = str(request.data.get('mobile'))           
        # print(email)
        try: 
            myuser=User.objects.get(id=id)
            print(myuser)
            if myuser is not None:
                myuser.first_name=firstname 
                myuser.last_name=lastname
                
                myuser.email=email
                                        
                myuser.mobile= str(mobile)
                myuser.save()
                return Response({'success':'Profile Update'},status=status.HTTP_200_OK)                            
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)


    