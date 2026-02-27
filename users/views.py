from rest_framework import generics, permissions, viewsets, permissions, status
from .serializers import UserSerializer, FollowSerializer
from rest_framework.response import Response
from .models import Follow, User

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny] # Регистрация доступна всем
    serializer_class = UserSerializer

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Текущий залогиненный юзер становится подписчиком
        serializer.save(follower=self.request.user)

    # Добавим метод для быстрой отписки
    def destroy(self, request, *args, **kwargs):
        follow_instance = self.get_object()
        if follow_instance.follower == request.user:
            follow_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Настраиваем права доступа:
        - Создание (регистрация): доступно всем.
        - Просмотр: доступно всем авторизованным.
        - Редактирование/Удаление: только владельцу профиля.
        """
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()] # Можно добавить кастомный IsOwner
        return [permissions.IsAuthenticated()]