from django.urls import path
from battle.views import battle


urlpatterns = [
    path('battle/', battle, name='battle'),
]