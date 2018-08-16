# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, "inicio.html", {})


def login_aplicacao(request):

    form = AuthenticationForm(request)

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            # if request.user.is_superuser:
            #     return HttpResponseRedirect(reverse('administracao:index'))

            return render(request, 'inicio.html', {})
        else:
            messages.warning(request, "Login/senha incorretos ou seu login está inativo")

    return render(request, 'login.html', {'form': form})
