from django.urls import path, include
from . import views


urlpatterns = [
    path('users/', views.ProfileWeightImcListCreateView.as_view(),
        name='user-list-create'),
    path('users/<str:username>/imc/', views.ProfileImcRetrieveView.as_view(),
        name='imc-list-create'),
    path('users/<str:username>/weight',
        views.ProfileWeightRetrieveView.as_view(),
        name='user-weight-history'),
]
