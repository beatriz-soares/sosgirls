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
from comum.forms import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def paginar_registros(request, registros, qtd_por_pagina):
    paginator = Paginator(registros, qtd_por_pagina)
    page = request.GET.get('page')

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

def index(request):
    if request.user.is_authenticated():
        registros = Depoimentos.objects.all().order_by("-id")
        # form = FiltroTelediagnosticoForm(request.GET or None)
        # if request.GET and form.is_valid():
        #     mes_referencia = form.cleaned_data.get('mes_referencia')
        #     data_inicio_exame = form.cleaned_data.get('data_inicial_exame')
        #     data_fim_exame = form.cleaned_data.get('data_final_exame')
        #     data_inicio_laudo = form.cleaned_data.get('data_inicial_laudo')
        #     data_fim_laudo = form.cleaned_data.get('data_final_laudo')
        #
        #     if mes_referencia:
        #         registros = registros.filter(conjunto_indicadores__mes_referencia=mes_referencia.strftime("%m%Y"))
        #     if data_inicio_exame:
        #         registros = registros.filter(data_exame__date__gte=data_inicio_exame)
        #     if data_fim_exame:
        #         registros = registros.filter(data_exame__date__lte=data_fim_exame)
        #     if data_inicio_laudo:
        #         registros = registros.filter(data_laudo__date__gte=data_inicio_laudo)
        #     if data_fim_laudo:
        #         registros = registros.filter(data_laudo__date__lte=data_fim_laudo)
        depoimentos = paginar_registros(request, registros, 15)
        # return render(request, 'comum/listagem_telediagnosticos.html', {'telediagnosticos': telediagnosticos, 'form': form})
        return render(request, "inicio.html", {"depoimentos":depoimentos})
    else:
        return HttpResponseRedirect(reverse('comum:login'))


def login_aplicacao(request):
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect(reverse('comum:index'))

    form = AuthenticationForm(request)

    if request.POST:
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            # if request.user.is_superuser:
            #     return HttpResponseRedirect(reverse('administracao:index'))

            return HttpResponseRedirect(reverse('comum:index'))
        else:
            messages.warning(request, "Login/senha incorretos ou seu login está inativo")

    return render(request, 'login.html', {'form': form})

def logout_aplicacao(request):
    logout(request)
    return HttpResponseRedirect(reverse('comum:index'))

def novo_depoimento(request):
    form = NovoDepoimentoForm(request.POST or None)
    if request.POST and form.is_valid():
        depoimento = form.save(commit=False)
        depoimento.autor = request.user
        depoimento.save()
        messages.success(request, "Seu depoimento foi postado!")
        return HttpResponseRedirect(reverse('comum:index'))

    return render(request, 'novo_depoimento.html', {"form":form})

def novo_comentario(request, id):
    if request.GET:
        conteudo = request.GET["comentario"]
        depoimento = Depoimentos.objects.get(pk=id)
        Comentario.objects.create(autor=request.user, pai=depoimento, conteudo=conteudo)
        messages.success(request, u"Seu comentário foi postado!")
        return HttpResponseRedirect(reverse('comum:index'))
