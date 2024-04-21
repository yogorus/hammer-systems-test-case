from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User, Referral


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='RU', required=True)

    class Meta:
        fields = '__all__'


class RegisterUserSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(required=True)

    class Meta:
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(region='RU', required=True)
    is_activated = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referral
