from django.urls import path
from battle.views import battle, choose, not_authenticated, index, battle_temp, choose_temp, user_logged_in_


urlpatterns = [
    path('', index, name='index'),
    path('battle/', battle, name='battle'),
    path('choose/', choose, name='choose'),
    path('not_authenticated/', not_authenticated, name='not_authenticated'),

    path('battletemp/', battle_temp, name='battle_temp'),
    path('choosetemp/', choose_temp, name='choose_temp'),

    path('oauth/', user_logged_in_),  # used to trigger view that retrieves auth data

]
