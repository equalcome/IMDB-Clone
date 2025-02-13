from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.authtoken.models import Token  # Token 模型的主要字段：key user created
from user_app import models


@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST',])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            # 回傳註冊的account (跟一個Token token是models裡面的create_auth_token方法產生出來的)
            account = serializer.save()

            data['response'] = "Registration Successful!!!"
            data['username'] = account.username
            data['email'] = account.email

            # 把User的Token拿出來 # Token.objects.get(user_id=account.id).key
            token = Token.objects.get(user=account).key
            data['token'] = token  # 放到data裡

            # JWT
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }

        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)
