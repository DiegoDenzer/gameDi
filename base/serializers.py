from django.contrib.auth.models import User
from rest_framework import serializers

from base.models.classe import Classe


class ClasseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
