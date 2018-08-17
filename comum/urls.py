from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^inicio/', views.index, name='index'),
    url(r'^login/', views.login_aplicacao, name='login'),
    url(r'^logout/', views.logout_aplicacao, name='logout'),
    url(r'^novo_depoimento/', views.novo_depoimento, name='novo_depoimento'),
]
