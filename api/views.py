from goals.models import User, Goal
from rest_framework import generics
from api.serializers import (
    UserCreateSerializer, UserSerializer,
    GoalSerializer
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny


@api_view(['GET', ])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'goals': reverse('goal-list', request=request, format=format),
    })


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


class GoalListView(generics.ListCreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
