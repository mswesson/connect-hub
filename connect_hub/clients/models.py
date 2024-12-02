from django.db import models
from django.forms import ValidationError
import random
import string
import re
from django.contrib.auth.models import User


def validate_phone_number(value) -> None | ValidationError:
    """
    ## Кастомный валидатор для номера телефона

    Проверяет, что номер телефона соответствует следующим условиям:
    - Начинается с символа +.
    - Содержит от 9 до 15 цифр после +.

    ### Результат
    Если номер телефона соответствует требованиям, функция
    завершает выполнение без ошибок.
    Если требования не соблюдаются, выбрасывается исключение
    ValidationError с соответствующим описанием ошибки.
    """
    if not re.match(r"^\+\d{9,15}$", value):
        raise ValidationError(
            'Please enter a valid phone number that starts with "+"'
        )


def random_invite_code() -> str:
    """
    ## Генерирует случайный пригласительный код

    Делает проверку после создания кода, на то что такого кода не существует

    ### Результат
    Выводит строку длинной 6 символов
    """

    characters = string.ascii_letters + string.digits

    while True:
        invitation_code = "".join(random.choices(characters, k=6))

        try:
            Client.objects.get(invitation_code=invitation_code)
        except Client.DoesNotExist:
            return invitation_code


class Client(models.Model):
    """
    ## Модель клиента

    ### Содержит в себе информацию:
    - Идентификационынй номер (id)
    - Номер телефона
    - Собственный пригласительный код
    - Введенный чужой пригласительный код
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,
    )
    phone = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        validators=[validate_phone_number],
        unique=True,
    )
    invitation_code = models.CharField(
        max_length=6,
        null=False,
        blank=True,
        default=random_invite_code,
        unique=True,
    )
    someone_invitation_code = models.CharField(
        max_length=6, null=True, blank=True
    )

    def __str__(self):
        return self.phone

    def save(
        self,
        *args,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        if not self.user:
            user = User.objects.create_user(
                username=self.phone, password="123456qQ"
            )
            self.user = user

        return super().save()


class ClientConnections(models.Model):
    """
    ## Модель связи клиентов

    ### Содержит в себе информацию:
    - Идентификационынй номер связи (id)
    - Идентификационынй номер приглашенного клиента (id)
    - Идентификационынй номер пригласившего клиента (id)
    """

    invited_client = models.ForeignKey(
        Client,
        related_name="inviter_client",
        on_delete=models.CASCADE,
        unique=True,
    )
    inviter_client = models.ForeignKey(
        Client,
        related_name="connections_invited_clients",
        on_delete=models.CASCADE,
    )
