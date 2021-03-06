from rest_framework import serializers
from users.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """ User Serializer
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'image',
        )
        read_only_fields = ('image',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    """ Update User Serializer
    """
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'image',
        )
        read_only_fields = ('image',)


class LoginSerializer(serializers.Serializer):
    """ Login Serializer.
    """
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    token = serializers.ReadOnlyField(required=False)
    user_cache = None


    def validate(self, user_data):
        user = authenticate(**user_data)
        if not user:
            raise serializers.ValidationError('Invalid Email or Password.')
        self.user_cache = user
        token, create = Token.objects.get_or_create(user=user)
        user_data['token'] = token.key
        return user_data
