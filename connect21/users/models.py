from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from .tasks import send_two_factor_code_email_task
import random


class User(AbstractUser):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский')
    ]
    surname = models.CharField(max_length=128)
    tg_username = models.CharField(max_length=128)
    age = models.IntegerField()
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return self.username

    @staticmethod
    def generate_code():
        code = random.randint(100000, 999999)
        return code

    def send_verification_email(self, code):
        subject = f'Код подтверждения для {self.username}'
        message = (
            f'Ваш код подтверждения: {code}\n'
            'С уважением, команда School21'
        )
        send_two_factor_code_email_task.delay(subject, message, self.email)
