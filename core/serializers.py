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
    # this should make sure that emails are unique
    email = serializers.EmailField(required=True, allow_blank=False)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'birth_date', 'groups', 'user_permissions', 'profile_picture']

    
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ['id', 'groups', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        groups = validated_data.pop('groups', None)
        user_permissions = validated_data.pop('user_permissions', None)
        
    
        user = User.objects.create_user(**validated_data)
        user.is_active = True
        user.save()
        if groups:
            user.groups.set(groups)
        if user_permissions:
            user.user_permissions.set(user_permissions)
        
        return user