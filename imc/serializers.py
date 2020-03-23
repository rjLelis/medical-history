from datetime import date

from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Imc, Profile, WeightHistory

class WeightHistorySerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='created_at',
        format='%d/%m/%Y %H:%M:%S',
        read_only=True)

    class Meta:
        model = WeightHistory
        fields = ('weight', 'date')
        extra_kwargs = {
            'weight': {'read_only': True},
        }


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

    classificacao_imc = serializers.CharField(
        source='get_classificacao_display',
        read_only=True
    )

    class Meta:
        model = Imc
        fields = ('height', 'weight', 'imc', 'classificacao_imc',)
        extra_kwargs = {
            'imc': {'read_only': True}
        }


class ProfileWeightSerializer(serializers.ModelSerializer):

    weight_history = serializers.SerializerMethodField()

    def get_weight_history(self, instance):
        weight_history = instance.weight_history.all().order_by('-created_at')
        return WeightHistorySerializer(
            weight_history,
            many=True,
            read_only=True
        ).data

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email', 'weight_history')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
        }


class ProfileImcSerializer(serializers.ModelSerializer):

    imc = ImcSerializer()

    class Meta:
        model = Profile
        fields = ('username', 'full_name', 'age', 'email', 'imc')
        extra_kwargs = {
            'username': {'read_only': True}
        }


class ProfileWeightImcSerializer(serializers.HyperlinkedModelSerializer):

    imc_url = serializers.HyperlinkedIdentityField(
        view_name='user-imc-retrieve',
        lookup_field='username'
    )

    weight_history_url = serializers.HyperlinkedIdentityField(
        view_name='user-weight-history-retrieve',
        lookup_field='username'
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
            'url',
            'imc_url',
            'weight_history_url'
        )
        extra_kwargs = {
            'url': {
                'view_name': 'user-retrieve-update',
                'lookup_field': 'username'
            },
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'date_of_birth': {
                'required': False,
                'write_only': True
            },
        }

    def create(self, validated_data):
        imc = validated_data.pop('imc')

        profile = Profile.objects.create(**validated_data)

        Imc.objects.create(user=profile, **imc)

        return profile


class ProfileWeightImcUpdateSerializer(serializers.ModelSerializer):

    imc = ImcSerializer()

    weight_history = serializers.SerializerMethodField()

    def get_weight_history(self, instance):
        weight_history = instance.weight_history.all().order_by('-created_at')
        return WeightHistorySerializer(
            weight_history,
            many=True,
            read_only=True
        ).data

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
        extra_kwargs = {
            'date_of_birth': {'write_only': True}
        }

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


            profile_email = validated_data.pop(
                'email',
                instance.email
            )

            profile_date_of_birth = validated_data.pop('date_of_birth')

            profile.first_name = profile_first_name
            profile.last_name = profile_last_name
            profile.date_of_birth = profile_date_of_birth \
                if profile_date_of_birth else instance.date_of_birth

            profile.email = profile_email

            profile.save()

        except (Profile.DoesNotExist, Imc.DoesNotExist):

            return Response({
                'message': f'user with username {instance.username} not found'
            }, status=status.HTTP_404_NOT_FOUND)

        return profile
