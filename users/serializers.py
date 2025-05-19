from rest_framework import serializers, views, status
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "user_country",
            "user_photo",
            "password",
            "telegram_profile",
            "telegram_chat_id",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных пользователя"""

    class Meta:
        model = User
        fields = ["phone_number", "user_country", "user_photo", "telegram_chat_id"]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токена"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email

        return token
