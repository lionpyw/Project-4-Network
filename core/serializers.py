from djoser.serializers import UserSerializer as BaseUserSerializer, \
UserCreateSerializer as BaseUserCreateSerializer, UserCreatePasswordRetypeSerializer
from .models import User


class UserCreateSerializer(UserCreatePasswordRetypeSerializer):
    
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username','email',
                   'first_name', 'last_name', 'password']


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ['id','username','email','first_name','last_name',
                   'is_service_provider'
                   ]