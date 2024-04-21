from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import PhoneNumberSerializer, RegisterUserSerializer, UserSerializer
from .models import User
import time
import random

# Create your views here.


class PhoneNumberAuthView(generics.GenericAPIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get('phone_number')

            verification_code = random.randint(1000, 9999)

            # Имитация отправки кода
            # Сохранить номер и код в куки для дальнейшей верификации (имитация того что мы реально это где-то проверяем)

            time.sleep(2)

            data = {
                'verification_code': verification_code,
                'phone_number': str(phone_number)
            }

            response = Response()
            response.set_cookie(key='phone_number', value=data['phone_number'], max_age=15)
            response.set_cookie(key='verification_code', value=data['verification_code'], max_age=15)
            response.data = data

            return response


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request):
        try:
            data = request.data
            cookie_phone_number = request.COOKIES['phone_number']
            cookie_verification_code = request.COOKIES['verification_code']

            if cookie_verification_code == data['verification_code']:

                # CREATE user
                user_serializer = UserSerializer(data={'phone_number': cookie_phone_number})
                user_serializer.is_valid(raise_exception=True)
                self.perform_create(user_serializer)
                return Response(user_serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'invalid_code'}, status=status.HTTP_400_BAD_REQUEST)

        except KeyError:
            return Response({'message': 'code expired'}, status=status.HTTP_410_GONE)