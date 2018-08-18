from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^inicio/', views.index, name='index'),
    url(r'^login/', views.login_aplicacao, name='login'),
    url(r'^logout/', views.logout_aplicacao, name='logout'),
    url(r'^novo_depoimento/', views.novo_depoimento, name='novo_depoimento'),
    url(r'^novo_comentario/(?P<id>\d+)/$', views.novo_comentario, name='novo_comentario'),
    url(r'^nova_mensagem/(?P<id>\d+)/$', views.nova_mensagem, name='nova_mensagem'),
    url(r'^mensagens/$', views.ver_mensagens, name='mensagens'),
    url(r'^mensagens/(?P<id>\d+)/$', views.mensagens, name='mensagens'),
    url(r'^tipos_depoimento/$', views.tipos_depoimento, name='tipos_depoimento'),
    url(r'^tipos_depoimento/novo/$', views.novo_tipo_depoimento, name='novo_tipo_depoimento')
]
