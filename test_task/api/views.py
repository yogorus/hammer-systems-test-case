from django.shortcuts import render
from rest_framework import generics, status, mixins, viewsets
from rest_framework.response import Response
from .serializers import PhoneNumberSerializer, RegisterUserSerializer, UserSerializer, ReferralSerializer
from .models import User, Referral
import time
import random


class PhoneNumberAuthView(generics.GenericAPIView):
    serializer_class = PhoneNumberSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.validated_data.get('phone_number')

            if User.objects.filter(phone_number=phone_number):
                return Response(
                    {'message': 'user with this number already exists'},
                    status=status.HTTP_409_CONFLICT
                )

            verification_code = random.randint(1000, 9999)

            # Имитация отправки кода
            # Сохранить номер и код в куки для дальнейшей верификации (имитация того что мы реально это где-то проверяем)

            time.sleep(1)

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

                if User.objects.filter(phone_number=cookie_phone_number).exists():
                    return Response(
                        {'message': 'user with this phone number already exists'},
                        status=status.HTTP_409_CONFLICT)

                self.perform_create(user_serializer)
                return Response(user_serializer.data,
                                status=status.HTTP_201_CREATED)

            return Response(
                {'message': 'invalid_code'},
                status=status.HTTP_400_BAD_REQUEST
                )

        except KeyError:
            return Response(
                {'message': 'code expired'},
                status=status.HTTP_410_GONE
                )


class UserView(mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    serializer_class = UserSerializer
    activate_serializer_class = ReferralSerializer
    queryset = User.objects.all()

    def update(self, request, *args, **kwargs):
        data = request.data
        code = data['code']
        user = self.get_object()

        if user.is_activated:
            return Response(
                {'message': 'user is already activated'},
                status=status.HTTP_409_CONFLICT
                )

        referral = generics.get_object_or_404(Referral, code=code)

        if referral.owner == user:
            return Response(
                {'message': "you can't activate your own code"},
                status=status.HTTP_400_BAD_REQUEST
            )
        # if success
        user.is_activated = True
        user.invited_by = referral

        user.save()
        serializer = UserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def get_serializer_class(self):
        if self.action == 'update':
            if hasattr(self, 'activate_serializer_class'):
                return self.activate_serializer_class

        return super(UserView, self).get_serializer_class()
