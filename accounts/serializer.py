from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'last_name', 'first_name']


class CheckAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_superuser', 'is_staff']


class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Проверка на существование пользователя по электронной почте или имени пользователя
        if User.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError(
                {'email': 'Пользователь с таким адресом электронной почты уже существует'})
        if User.objects.filter(username__iexact=validated_data['username']).exists():
            raise serializers.ValidationError({'username': 'Пользователь с таким username уже существует'})

        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user