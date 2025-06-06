import os
from django.urls import reverse
import requests
from django.shortcuts import redirect
from social_core.backends.oauth import BaseOAuth2

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")


class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    def authorization_url(self):
        """Return the authorization endpoint."""
        return "https://" + self.setting('DOMAIN') + "/authorize"


    def access_token_url(self):
        """Return the token endpoint."""
        return "https://" + self.setting('DOMAIN') + "/oauth/token"


    def get_user_id(self, details, response):
        """Return current user id."""
        return details['user_id']


    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        
        return {
            'username': userinfo['nickname'],
            'first_name': userinfo['name'],
            'picture': userinfo['picture'],
            'user_id': userinfo['sub'],
        }


# Esta función está fuera de la clase Auth0. Es independiente.
def getRole(request):
    user = request.user
    if not user.is_authenticated:
        print("User is not authenticated")
        return redirect('social:begin', 'auth0')
    if not user.social_auth.exists():
        print("User social auth does not exist")
        return redirect('social:begin', 'auth0')
    auth0user = user.social_auth.filter(provider="auth0")[0]  

    accessToken = auth0user.extra_data['access_token'] 
    url = f"https://{AUTH0_DOMAIN}/userinfo" 
    headers = {'authorization': 'Bearer ' + accessToken}

    resp = requests.get(url, headers=headers)

    userinfo = resp.json()

    role = userinfo[f'{AUTH0_DOMAIN}/role']

    return (role)

