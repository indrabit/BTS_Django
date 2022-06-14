
from dataclasses import field, fields
from pyexpat import model
from rest_framework.authtoken.models import Token
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.password_validation import validate_password
from django.contrib import auth
from django.contrib.auth import authenticate
from .models import User

from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response

    
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    # redirect_url = serializers.CharField(max_length=500, required=False)
    class Meta:
        fields=['email']
        
        
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)

class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    userid=serializers.IntegerField()
    password_new=serializers.CharField()
    password_old=serializers.CharField()

    def create(self, validated_data):
        pass
    def update(self, instance, validated_data):
        pass
    



