from rest_framework import generics
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from django.core.mail import send_mail
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# регистрация пользователя при помощи JWT
class RegisterUser(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @swagger_auto_schema(operation_summary="Регистрация пользователя",
                         operation_description="Для неавторизованных пользователей. Создает новый аккаунт по никнейму, адресу электронной почты и паролю")
    def post(self, request, *args, **kwargs):
        # валидация на существующего пользователя
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data
        })


# Выход из аккаунта
class LogoutView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_summary="Выход из аккаунта",
                         operation_description="Для авторизованных пользователей",
                         tags=["accounts"],
                         responses={200: "Успешный выход из аккаунта"})
    def put(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully'})


# проверка роли администратора
class CheckAdminView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_summary="Проверка роли администратора",
                         operation_description="Для авторизованных пользователей. Проверяет, имеет ли пользователь роль администратора 1го или 2го уровня, для доступа к тому или иному функционалу на клиенте приложения",
                         responses={200: CheckAdminSerializer})
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = CheckAdminSerializer(user)
        return Response(serializer.data)


# получение данных пользователя
class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_summary="Получение данных пользователя",
                         operation_description="Для авторизованных пользователей. Получение данных для просмотра и редактирования своего профиля",
                         responses={200: UserSerializer})
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


update_user_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='Адрес электронной почты'),
        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Фамилия'),
        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя'),
    },
)

# изменение данных пользователя
class UserUpdateView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(operation_summary="Редактирование профиля",
                         operation_description="Для авторизованных пользователей. Изменение своих данных профиля",
                         request_body=update_user_schema,
                         responses={
                             200: UserSerializer(),
                             400: "Ошибка (невалидные поля профиля пользователя)",
                         }
                         )
    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


send_email_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['email'],
    properties={
        'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='Адрес электронной почты'),
    },
)

# восстановление пароля по почте
class EmailForPassword(APIView):
    parser_classes = [JSONParser]

    @swagger_auto_schema(operation_summary="Отправка письма для восстановления пароля",
                         operation_description="Для авторизованных пользователей. Позволяет восстановить пароль по ссылке из письма",
                         request_body=send_email_schema,
                         responses={
                             200: "Отправлено",
                             400: "Ошибка (невалидные данные)",
                         })
    def put(self, request):
        try:
            data = request.data
            email = data['email']
            subject = 'MusicHome. Восстановление пароля.'
            message = f'Здравствуйте!\n\nВы запросили сброс пароля для своего аккаунта на musicHome.\nЧтобы восстановить пароль, перейдите по этой ссылке:\n\nhttp://localhost:8000/reset-password/hg12Sa2\n\nЕсли вы не запрашивали сброс пароля, проигнорируйте это письмо.\n\nС уважением, команда MusicHome.'
            from_email = 'musichomeforyou@gmail.com'
            # password = 'f1BLhKKiv3EXCVY9UY3H'
            recipient_list = [email]
            sending = "Отправлено!"
            send_mail(subject, message, from_email, recipient_list)

            return Response({"status": "success", "message": sending}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)