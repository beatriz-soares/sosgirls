from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^inicio/', views.index, name='index'),
    url(r'^login/', views.login_aplicacao, name='login'),
]
