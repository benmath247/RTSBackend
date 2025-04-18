from rest_framework import serializers
from .models import FavoriteStock

class FavoriteStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteStock
        fields = ['id', 'user', 'stock_symbol', 'added_on']
        read_only_fields = ['id', 'added_on']


from rest_framework import serializers
from core.models import User

class UserSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(format='%Y/%m/%d', input_formats=['%Y/%m/%d'], required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'birth_date', 'groups', 'user_permissions', 'profile_picture']

    def create(self, validated_data):
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        user = User.objects.create_user(**validated_data)
        
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)
        
        return user