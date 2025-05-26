from django.conf.urls import url
from .views import eventos

urlpatterns = [
    url(r'^eventos/$', eventos),
]