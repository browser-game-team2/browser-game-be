###
# here we can write a class with methods to retrieve authentication data from db
###

from django.shortcuts import render
import json
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialToken
# from battle.battle_package.request import Request
# from battle.battle_package.algorithm import BattleAlgo
# from battle.battle_package.response import Response


class UserAuth:

    def __init__(self, request):
        self.user = User.objects.get(username=request.user)
        self.username = self.user.username
        self.social_account = SocialAccount.objects.get(user_id=self.user.id)
        self.uid = self.social_account.uid
        self.social_token = SocialToken.objects.get(account_id=self.social_account.id)
        self.token = self.social_token.token

    '''
    @staticmethod
    def get_user(request):
        return User.objects.get(username=request.user)  # request.user will be the Google username

    @staticmethod
    def get_username(user_db):
        return user_db.username

    @staticmethod
    def get_social_account(user_db):
        return SocialAccount.objects.get(user_id=user_db.id)

    @staticmethod
    def get_uid(social_account_db):
        return social_account_db.uid

    @staticmethod
    def get_social_token(social_account_db):
        return SocialToken.objects.get(account_id=social_account_db.id)

    @staticmethod
    def get_token(social_token_db):
        return social_token_db.token
    '''