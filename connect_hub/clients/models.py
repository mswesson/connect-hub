from django.db import models
from django.forms import ValidationError
import re


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


class Client(models.Model):
    """
    ## Модель клиента

    ### Содержит в себе информацию:
    - Идентификационынй номер (id)
    - Номер телефона
    - Собственный пригласительный код
    - Введенный чужой пригласительный код
    """

    phone = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        validators=[validate_phone_number],
    )


class ClientConnections(models.Model):
    """
    ## Модель связи клиентов

    ### Содержит в себе информацию:
    - Идентификационынй номер связи (id)
    - Идентификационынй номер приглашенного клиента (id)
    - Идентификационынй номер пригласившего клиента (id)
    """

    invited_client = models.ForeignKey(
        Client, related_name="inviter_client", on_delete=models.CASCADE
    )
    inviter_client = models.ForeignKey(
        Client, related_name="invited_clients", on_delete=models.CASCADE
    )
