from datetime import date

from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Imc, Profile, WeightHistory
from .serializers_utils import BaseProfile


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


class ProfileWeightSerializer(serializers.ModelSerializer,
    BaseProfile):

    full_name = serializers.SerializerMethodField(source='get_full_name')

    age = serializers.SerializerMethodField(source='get_age')

    weight_history = WeightHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email', 'weight_history')


class ProfileImcSerializer(serializers.ModelSerializer,
    BaseProfile):

    full_name = serializers.SerializerMethodField(source='get_full_name')

    age = serializers.SerializerMethodField(source='get_age')

    imc = ImcSerializer()

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email', 'imc')


class ProfileWeightImcSerializer(serializers.ModelSerializer,
    BaseProfile):

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

    date_of_birth = serializers.DateField(write_only=True, required=False)

    imc = ImcSerializer()

    weight_history = WeightHistorySerializer(
        many=True,
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


    def create(self, validated_data):

        imc = validated_data.pop('imc')

        profile = Profile.objects.create(**validated_data)

        Imc.objects.create(user=profile,**imc)

        return profile


class ProfileWeightImcUpdateSerializer(serializers.ModelSerializer,
    BaseProfile):


    full_name = serializers.SerializerMethodField(
        source='get_full_name',
        read_only=True
    )

    age = serializers.SerializerMethodField(
        source='get_age',
        read_only=True
    )

    date_of_birth = serializers.DateField(write_only=True)

    imc = ImcSerializer()

    weight_history = WeightHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'full_name',
            'age',
            'first_name',
            'last_name',
            'date_of_birth',
            'email',
            'imc',
            'weight_history',
        )

    def update(self, instance, validated_data):

        try:

            imc_values = validated_data.pop('imc')

            if imc_values:
                current_height = imc_values.get(
                    'current_height',
                    instance.imc.current_height
                )

                current_weight = imc_values.get(
                    'current_weight',
                    instance.imc.current_weight
                )

                imc = Imc.objects.get(user=instance)
                imc.current_height = current_height
                imc.current_weight = current_weight
                imc.save()

            profile = Profile.objects.get(username=instance.username)

            profile_first_name = validated_data.pop(
                'first_name',
                instance.first_name
            )

            profile_last_name = validated_data.pop(
                'last_name',
                instance.last_name
            )

            profile_date_of_birth = validated_data.pop(
                'date_of_birth',
                instance.date_of_birth
            )

            profile_email = validated_data.pop(
                'email',
                instance.email
            )

            profile.first_name = profile_first_name
            profile.last_name = profile_last_name
            profile.date_of_birth = profile_date_of_birth
            profile.email = profile_email

            profile.save()

        except (Profile.DoesNotExist, Imc.DoesNotExist):

            return Response({
                'message': f'user with username {instance.username} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        return profile
