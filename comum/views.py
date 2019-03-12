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
from django.http import JsonResponse
from django.forms import inlineformset_factory

def editar_vinculos_formset(extra=0):
    return inlineformset_factory(Depoimentos, Comentario, form=CadastroCommentForm,
                                 can_delete=True, extra=extra, max_num=15,
                                 fields=('conteudo', 'autor'))

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
        form = FiltroDepoimentoForm(request.GET or None)
        if request.GET and form.is_valid():
            tipo = form.cleaned_data.get('tipo')
            if tipo:
                registros = registros.filter(tipo=tipo)
        depoimentos = paginar_registros(request, registros, 15)
        # return render(request, 'comum/listagem_telediagnosticos.html', {'telediagnosticos': telediagnosticos, 'form': form})
        return render(request, "inicio.html", {"depoimentos":depoimentos, "form":form})
    else:
        return HttpResponseRedirect(reverse('comum:login'))

def novo_usuario(request):
    form = NovoUserForm(request.POST or None)
    if request.POST and form.is_valid():
        depoimento = form.save()
        messages.success(request, "Novo usuário cadastrado! Você já pode fazer login")
        return HttpResponseRedirect(reverse('comum:index'))

    return render(request, "novo_usuario.html", {"form":form})


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
    form = NovoDepoimentoForm(request.POST or None, request.FILES or None)
    if request.POST and form.is_valid():
        depoimento = form.save(commit=False)
        depoimento.autor = request.user
        depoimento.save()
        messages.success(request, "Seu depoimento foi postado!")
        return HttpResponseRedirect(reverse('comum:index'))

    return render(request, 'novo_depoimento.html', {"form":form})

def tipos_depoimento(request):
    if request.user.is_superuser:
        registros = TipoDepoimentos.objects.all().order_by("-id")
        depoimentos = paginar_registros(request, registros, 15)
        return render(request, "tipos_depoimento.html", {"depoimentos":depoimentos})
    else:
        return HttpResponseRedirect(reverse('comum:index'))

def novo_tipo_depoimento(request):
    if request.user.is_superuser:
        form = NovoTipoDepoimentoForm(request.POST or None)
        if request.POST and form.is_valid():
            depoimento = form.save()
            messages.success(request, "Novo tipo de depoimento salvo!")
            return HttpResponseRedirect(reverse('comum:tipos_depoimento'))

        return render(request, 'novo_tipo_depoimento.html', {"form":form})
    else:
        return HttpResponseRedirect(reverse('comum:index'))

def novo_comentario(request, id):
    profissional = Depoimentos.objects.get(pk=id)
    EditarVinculoFormSet = editar_vinculos_formset()
    vinculo_form = EditarVinculoFormSet(request.POST or None, instance=profissional)
    if request.POST:
        if vinculo_form.is_valid():
                vinculo_form.save()
        else:
            print "ERROOOOO"
            messages.warning(request, u"Verifique os dados inseridos")
            return render(request, "inaldo.html", locals())
    return render(request, "inaldo.html", locals())

def apagar_depoimento(request, id):
    depoimento = Depoimentos.objects.get(pk=id).delete()
    messages.success(request, u"O depoimento foi apagado!")
    return HttpResponseRedirect(reverse('comum:index'))

def nova_mensagem(request, id):
    if request.POST:
        conteudo = request.POST["msgm"]
        depoimento = Depoimentos.objects.get(pk=id)
        Mensagem.objects.create(autor=request.user, destinatario=depoimento.autor, conteudo=conteudo, lida=False)
        messages.success(request, u"Sua mensagem foi enviada ao autor do depoimento!")
        return HttpResponseRedirect(reverse('comum:index'))

def ver_mensagens(request):
    registros = Mensagem.objects.filter(destinatario=request.user).order_by("-id")
    mensagens = paginar_registros(request, registros, 15)
    return render(request, 'ver_mensagens.html', {"mensagens":mensagens})

def mensagens(request, id):
    mensagem = Mensagem.objects.get(pk=id)
    mensagem.lida=True
    mensagem.save()
    return JsonResponse({"conteudo":mensagem.conteudo})

def estatistica(request):
    total_count = Depoimentos.objects.all().count()
    percentuais = []
    for tipo in TipoDepoimentos.objects.all():
        cnt = Depoimentos.objects.filter(tipo=tipo).count()
        perc = cnt * 100 / total_count
        percentuais.append({"nome": tipo.nome, "percentual":perc})
    return render(request, 'estatistica.html', {"percentuais":percentuais})
