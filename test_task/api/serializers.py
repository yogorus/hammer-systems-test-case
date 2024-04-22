from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from phonenumber_field.phonenumber import to_python
from rest_framework.exceptions import ValidationError
from .models import User, Referral


class PhoneNumberFieldSerializable(PhoneNumberField):

    def to_internal_value(self, data):
        phone_number = to_python(data)
        if phone_number and not phone_number.is_valid():
            raise ValidationError(self.error_messages["invalid"])
        return phone_number.as_e164


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(region='RU', required=True)

    class Meta:
        fields = '__all__'


class RegisterUserSerializer(serializers.Serializer):
    verification_code = serializers.IntegerField(required=True)

    class Meta:
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    invited_users = serializers.SlugRelatedField(many=True, slug_field='phone_number_str', read_only=True)
    # invited_users = UserSerializer()

    class Meta:
        model = Referral
        fields = ('code', 'invited_users')


class UserSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberFieldSerializable(region='RU', required=True)
    referral = serializers.SerializerMethodField()
    is_activated = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_referral(self, obj):
        referral = obj.referral.all().first()
        if referral:
            serializer = ReferralSerializer(referral)
            return serializer.data
