from rest_framework import filters, generics, status
from rest_framework import filters

from .models import Imc, Profile, WeightHistory
from . import serializers as imc_serializers


class ProfileWeightImcListCreateView(generics.ListCreateAPIView):

    queryset = Profile.objects.all()
    serializer_class = imc_serializers.ProfileWeightImcSerializer
    filter_backends = (filters.OrderingFilter, )
    ordering_fields = ('created_at', 'username')
    ordering = ('-created_at', )


class ProfileWeightImcRetrieveUpdateView(generics.RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    lookup_field = 'username'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return imc_serializers.ProfileWeightImcUpdateSerializer
        return imc_serializers.ProfileWeightImcSerializer

class ProfileImcRetrieveView(generics.RetrieveAPIView):

    queryset = Profile.objects.all()
    serializer_class = imc_serializers.ProfileImcSerializer
    lookup_field = 'username'


class ProfileWeightRetrieveView(generics.RetrieveAPIView):

    queryset = Profile.objects.all()
    serializer_class = imc_serializers.ProfileWeightSerializer
    lookup_field = 'username'

