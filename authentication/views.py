
from django.contrib.auth import authenticate,login
from django.db import connection
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authtoken.models import Token

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status,generics
from rest_framework.response import Response
from .serializer import ChangePasswordSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer

from .models import User
from datetime import datetime

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponsePermanentRedirect
import os
from django.contrib.auth import signals
from axes.handlers.proxy import AxesProxyHandler

import threading
from validate_email import validate_email
from django.core import mail


#login user
class EmailThread(threading.Thread):

    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()
        
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def Userlogin(request):
    email = request.data.get('email')
    password = request.data.get('password')
    # print(email) 
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    # create credentials to verify account locked
    credentials = {'username': email} 
    
    checkLocked=AxesProxyHandler.is_locked(request=request, credentials=credentials)     
    if checkLocked is True:
        return Response({'Account locked: too many login attempts. Please try again later.'}, status=status.HTTP_423_LOCKED)
    
        
    user = authenticate(request=request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        
        # New token update
        t = Token.objects.filter(user=user)
        print(t)
        print('test')
        if t is not None:
            new_key = t[0].generate_key()
            t.update(key=new_key)
            
        # get token if not null create token    
        token, _ = Token.objects.get_or_create(user=user)
        user.last_login = datetime.now()
        user.save()
        
        return Response({'username': {user.id},'token': {token.key}},status=status.HTTP_200_OK)
           
    signals.user_login_failed.send(sender=User,request=request,credentials=credentials)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    

#
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def create(request):
    email = str(request.data.get('email'))
    password = str(request.data.get('password'))
    username = str(request.data.get('username'))
    first_name = str(request.data.get('first_name'))
    last_name = str(request.data.get('last_name'))
    mobile = str(request.data.get('mobile'))
    
    
    user = User.objects.create_user(email, password, username,first_name,last_name)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response(
        {'token': {token.key}
                     }, status=status.HTTP_201_CREATED)


# Change paspword
class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class=ChangePasswordSerializer
    model=User
    permission_classes=(IsAuthenticated,)

    def get_object(self,queryset=None):
        obj=self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object=self.get_object
        serializer =self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_passwword": ["Wrong password ."]},status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestPasswordResetEmailView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            
            user = User.objects.get(email=email)
            # user id
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # token generate
            token = PasswordResetTokenGenerator().make_token(user)
            # user domian id
            current_site = get_current_site(
                request=request).domain
            # reverse linl
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url =  'http://'+current_site
            # request.data.get('redirect_url', '')
            absurl = 'http://'+current_site + relativeLink
            # message forward to client
            
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl+"?redirect_url="+redirect_url
            
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            
            print(data)
            # send email
            Util.send_email(data)    
            # EmailThread(data).start()    
            # connection=mail.get_connection()
            # connection.open()
            # email1 = mail.EmailMessage('Hello' 'Body goes here','ind_stha@yahoo.com',['indrabit@gmail.com'],connection=connection,)
            # email1.send()
            # connection.close()
            
        
        return Response({'success':'We have sent you a link to reset your password'},status=status.HTTP_205_RESET_CONTENT)
        
class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']
    
class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            # access user id
            id = smart_str(urlsafe_base64_decode(uidb64))
            # verify with user id
            user = User.objects.get(id=id)
            # check user id with get token
            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            
            
class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)
    
    