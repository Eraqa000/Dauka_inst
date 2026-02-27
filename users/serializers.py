from rest_framework import serializers
from .models import User, Follow

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=False, # Пароль не обязателен при обычном обновлении bio или avatar
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'bio', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Используем встроенный метод для создания и хэширования пароля
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        # Извлекаем пароль, если он есть в запросе (для PUT/PATCH)
        password = validated_data.pop('password', None)
        
        # Обновляем остальные поля (username, bio, email и т.д.)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Если пришел новый пароль, хэшируем его перед сохранением
        if password:
            instance.set_password(password)
            
        instance.save()
        return instance

class FollowSerializer(serializers.ModelSerializer):
    # Добавим отображение имен, чтобы в GET запросе было понятно, кто на кого подписан
    follower_name = serializers.ReadOnlyField(source='follower.username')
    followee_name = serializers.ReadOnlyField(source='followee.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_name', 'followee', 'followee_name', 'created_at']
        read_only_fields = ['follower', 'created_at']