from django.urls import path, include
from . import views


urlpatterns = [
    path('v1/users/', views.ProfileWeightImcListCreateView.as_view(),
        name='user-list-create'),
    path('v1/users/<str:username>/',
        views.ProfileWeightImcRetrieveUpdateView.as_view(),
        name='user-retrieve-update'),
    path('v1/users/<str:username>/imc/',
        views.ProfileImcRetrieveView.as_view(),
        name='user-imc-retrieve'),
    path('v1/users/<str:username>/weight',
        views.ProfileWeightRetrieveView.as_view(),
        name='user-weight-history-retrieve'),
]
