from django.conf.urls import url
from .views import eventos, evento_detail, pacientes, paciente_detail, doctores, doctor_detail

urlpatterns = [
    url(r'^eventos/$', eventos),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/$', evento_detail),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/update/$', evento_detail),
    url(r'^eventos/(?P<evento_id>[a-zA-Z0-9]+)/delete/$', evento_detail),
    url(r'^pacientes/$', pacientes),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/$', paciente_detail),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/update/$', paciente_detail),
    url(r'^pacientes/(?P<paciente_id>[a-zA-Z0-9]+)/delete/$', paciente_detail),
    url(r'^doctores/$', doctores),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/$', doctor_detail),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/update/$', doctor_detail),
    url(r'^doctores/(?P<doctor_id>[a-zA-Z0-9]+)/delete/$', doctor_detail),

]