from django.urls import path
from battle.views import battle, choose, not_authenticated


urlpatterns = [
    path('battle/', battle, name='battle'),
    path('choose/', choose, name='choose'),
    path('not_authenticated/', not_authenticated, name='not_authenticated')
]