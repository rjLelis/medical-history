from datetime import date

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response

from . import utils
from .models import Imc, Profile, WeightHistory


class WeightHistorySerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(source='created_at')

    class Meta:
        model = WeightHistory
        fields = ('weight', 'date')


class ImcSerializer(serializers.ModelSerializer):

    height = serializers.DecimalField(
        source='current_height',
        max_digits=4,
        decimal_places=2
    )
    weight = serializers.DecimalField(
        source='current_weight',
        max_digits=5,
        decimal_places=2
    )

    imc = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        read_only=True
    )

    classificacao_imc = serializers.CharField(
        source='get_classificacao_display',
        read_only=True
    )

    class Meta:
        model = Imc
        fields = ('height', 'weight', 'imc', 'classificacao_imc', )


class ProfileWeightSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField(source='get_full_name')

    age = serializers.SerializerMethodField(source='get_age')

    weight_history = WeightHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email' ,'weight_history')


    def get_full_name(self, obj):
        return utils.get_profile_full_name(obj)


    def get_age(self, obj):
        return utils.get_profile_age(obj)


class ProfileImcSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField(source='get_full_name')

    age = serializers.SerializerMethodField(source='get_age')

    imc = ImcSerializer()

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email', 'imc')


    def get_full_name(self, obj):
        return utils.get_profile_full_name(obj)


    def get_age(self, obj):
        return utils.get_profile_age(obj)


class ProfileWeightImcSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField(
        source='get_full_name',
        read_only=True
    )

    age = serializers.SerializerMethodField(
        source='get_age',
        read_only=True
    )

    first_name = serializers.CharField(write_only=True)

    last_name = serializers.CharField(write_only=True)

    date_of_birth = serializers.DateField(write_only=True)

    imc = ImcSerializer()

    weight_history = WeightHistorySerializer(
        many=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = Profile
        fields = (
            'username',
            'first_name',
            'last_name',
            'date_of_birth',
            'full_name',
            'age',
            'email',
            'imc',
            'weight_history'
        )


    def get_full_name(self, obj):
        return utils.get_profile_full_name(obj)


    def get_age(self, obj):
        return utils.get_profile_age(obj)


    def create(self, validated_data):
        imc = validated_data.pop('imc')

        profile = Profile.objects.create(**validated_data)

        new_imc = Imc.objects.create(user=profile,**imc)

        return profile
