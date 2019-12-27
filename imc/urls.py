from django.urls import path, include
from . import views


urlpatterns = [
    path('v1/users/', views.ProfileWeightImcListCreateView.as_view(),
        name='user-list-create'),
    path('v1/users/<str:username>/imc/', views.ProfileImcRetrieveView.as_view(),
        name='imc-list-create'),
    path('v1/users/<str:username>/weight',
        views.ProfileWeightRetrieveView.as_view(),
        name='user-weight-history'),
    path('v1/users/<str:username>/',
        views.ProfileWeightImcRetrieveView.as_view(),
        name='user-retrieve-update'),
]
