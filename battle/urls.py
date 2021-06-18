from django.urls import path
from battle.views import battle, choose, not_authenticated, index


urlpatterns = [
    path('', index, name='index'),
    path('battle/', battle, name='battle'),
    path('choose/', choose, name='choose'),
    path('not_authenticated/', not_authenticated, name='not_authenticated')
]