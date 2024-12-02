from typing import Tuple
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from time import sleep
from random import randint
from django.core.cache import cache
from django.db.models import Q
import requests
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated


from .models import Client, ClientConnections
from .serializers import (
    ClientCreateSerializer,
    ClientProfileSerializer,
    ClientLoginSerializer,
)


class ClientCreateApiView(APIView):
    """
    ## Создание нового клиента

    ### Процесс создания:
    - Принимает в себя номер телефона
    - Генерирует СМС код и отправляет в ответ на запрос, отдает статус 200
    - В повторном запросе вместе с номером телефона отправляем СМС код
    - Если всё хорошо получаем ответ с информацией о новом
    клиенте и статус 201
    """

    def post(self, request: Request) -> Response:
        serializer = ClientCreateSerializer(data=request.data)
        phone = request.data.get("phone")
        cache_key = f"sms_code_{phone}"
        sms_code = request.data.get("sms_code")
        cache_sms_code = cache.get(cache_key)

        if not serializer.is_valid():
            return Response(
                data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        if not sms_code:
            sleep(1)

            sms_code = randint(1000, 9999)
            cache.set(
                key=cache_key,
                value=sms_code,
                timeout=100,
            )

            data = serializer.data
            data.update({"sms_code": sms_code})
            return Response(data=data, status=status.HTTP_200_OK)

        if sms_code != cache_sms_code:
            data = {"sms_code": "The code does not match or is outdated"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        req_data = {"username": phone, "password": "123456qQ"}

        url = request.build_absolute_uri(reverse("token_obtain_pair"))
        token = requests.post(url, json=req_data).json()
        token = token["access"]

        data = serializer.data
        data.update({"access_token": token})

        return Response(data, status=status.HTTP_201_CREATED)


class ClientLoginApiView(APIView):
    """
    ## Повторный вход

    Получение нового токена с помощью кода из смс

    ### Процесс создания:
    - Принимает в себя номер телефона
    - Генерирует СМС код и отправляет в ответ на запрос, отдает статус 200
    - В повторном запросе вместе с номером телефона отправляем СМС код
    - Если всё хорошо получаем ответ с информацией о клиенте,
    новый токен и статус 200
    """

    def post(self, request: Request) -> Response:
        phone = request.data.get("phone")
        cache_key = f"sms_code_{phone}"
        sms_code = request.data.get("sms_code")
        cache_sms_code = cache.get(cache_key)
        client = Client.objects.filter(phone=phone).first()

        if not client:
            data = {"error_message": "There is no user with this phone number"}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        if not sms_code:
            sleep(1)

            sms_code = randint(1000, 9999)
            cache.set(
                key=cache_key,
                value=sms_code,
                timeout=100,
            )

            data = {"phone": phone, "sms_code": sms_code}
            return Response(data=data, status=status.HTTP_200_OK)

        if sms_code != cache_sms_code:
            data = {"sms_code": "The code does not match or is outdated"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        req_data = {"username": phone, "password": "123456qQ"}

        url = request.build_absolute_uri(reverse("token_obtain_pair"))
        token = requests.post(url, json=req_data).json()
        token = token["access"]

        serializer = ClientLoginSerializer(client)
        data = serializer.data
        data.update({"access_token": token})

        return Response(data, status=status.HTTP_200_OK)


class ClientProfileApiView(APIView):
    """
    ## REST API представление

    Реализует основные методы работы с моделью Client
    - GET (просмотр клиента)
    - POST (создание клиента)
    - PATCH (добавление клиенту пригласительного кода)

    Дополнительные методы:
    - is_no_client_connection: проверяет связи между клиентами
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        ## Выдает информацию о клиенте

        Принимает в себя номер телефона клиента

        Выдает всю информацию о клиенте
        """

        client = request.user.profile
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request) -> Response:
        """
        ## Добавление клиенту кода пригласившего его пользвоателя

        Принимает 2 параметра:
        - телефон клиента
        - пригласительный код другого пользователя

        Производит проверку на сущестование кода и не был ли
        ранее присвоен другой код у клиента
        """

        someone_invitation_code = request.data.get("someone_invitation_code")
        invited_client = request.user.profile
        inviter_client = Client.objects.filter(
            invitation_code=someone_invitation_code
        ).first()

        if not invited_client:
            data = {"error_message": "No client with such a phone was found"}
            return Response(data, status=status.HTTP_409_CONFLICT)

        if not inviter_client:
            data = {
                "error_message": (
                    "The client with such an invitation code was not found"
                )
            }
            return Response(data, status=status.HTTP_409_CONFLICT)

        is_no_client_connection, data = self.is_no_client_connection(
            invited_client=invited_client,
            inviter_client=inviter_client,
        )

        if not is_no_client_connection:
            return Response(data, status=status.HTTP_409_CONFLICT)

        connections = ClientConnections(
            invited_client=invited_client,
            inviter_client=inviter_client,
        )
        invited_client.someone_invitation_code = someone_invitation_code

        invited_client.save()
        connections.save()

        serializer = ClientProfileSerializer(invited_client)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def is_no_client_connection(
        self, invited_client: Client, inviter_client: Client
    ) -> Tuple[bool, dict]:
        """
        ## Проверка связи между клиентами

        ### Результат
        - true - связи нет
        - false - связь есть

        Выводит кортеж *(булевое значение результата,
        сообщение в формате {"message": "text message"})*
        """
        client_connection = ClientConnections.objects.filter(
            Q(invited_client=invited_client, inviter_client=inviter_client)
            | Q(invited_client=inviter_client, inviter_client=invited_client)
        )

        if (
            invited_client.invitation_code
            == inviter_client.someone_invitation_code
        ):
            data = {"error_message": "Clients cannot invite each other"}
            return False, data

        elif client_connection:
            data = {
                "error_message": (
                    "The connection between the clients already exists"
                )
            }
            return False, data

        else:
            data = {
                "ok_message": "No connections were found between the clients"
            }
            return True, data
