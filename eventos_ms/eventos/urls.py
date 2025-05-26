from django.conf.urls import url
from .views import eventos

urlpatterns = [
    url(r'^eventos/$', eventos),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/$', eventos),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/update/$', eventos),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/delete/$', eventos),
    url(r'^pacientes/$', eventos),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/$', eventos),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/update/$', eventos),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/delete/$', eventos),
    url(r'^doctores/$', eventos),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/$', eventos),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/update/$', eventos),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/delete/$', eventos),
    
]