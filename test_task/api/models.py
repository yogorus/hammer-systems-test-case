from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField
from api.utils import generate_unique_code

# Create your models here.


class User(models.Model):
    phone_number = PhoneNumberField(unique=True)
    is_activated = models.BooleanField(default=False)
    invited_by = models.ForeignKey('Referral', related_name='invited_users', on_delete=models.CASCADE, blank=True, null=True)

    @property
    def phone_number_str(self):
        return str(self.phone_number)


class Referral(models.Model):
    owner = models.ForeignKey(User, related_name='referral', on_delete=models.CASCADE)
    code = models.CharField(primary_key=True, max_length=6, default=generate_unique_code)

# Создать реферальный код после регистрации юзера
@receiver(post_save, sender=User, dispatch_uid='user_post_save_signal')
def create_referral(sender, instance, created, **kwargs):
    if created:
        Referral.objects.create(owner=instance)
