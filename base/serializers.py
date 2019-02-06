from rest_framework import serializers

from base.models.classe import Classe


class ClasseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Classe
        fields = '__all__'
