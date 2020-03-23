from rest_framework import filters, generics, viewsets
from rest_framework.request import Request

from . import serializers as imc_serializers
from .models import Profile


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


class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = imc_serializers.ProfileWeightImcSerializer
    lookup_field = 'username'
