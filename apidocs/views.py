from django.http import Http404
from django.shortcuts import render

from .catalog import get_platform, get_section, get_stats, load_catalog


# ============================================================
# PORTAL DE DOCUMENTAÇÃO DAS APIS
# ============================================================
#
# Telas somente de leitura. Não acessam o banco de dados.

def home(request):
    context = {
        'platforms': load_catalog(),
        'stats': get_stats(),
        'current': 'home',
    }
    return render(request, 'apidocs/home.html', context)


def getting_started(request):
    context = {
        'platforms': load_catalog(),
        'current': 'getting-started',
    }
    return render(request, 'apidocs/getting_started.html', context)


def platform(request, plataforma):
    current_platform = get_platform(plataforma)
    if current_platform is None:
        raise Http404('Plataforma não encontrada')

    context = {
        'platforms': load_catalog(),
        'platform': current_platform,
        'current': plataforma,
    }
    return render(request, 'apidocs/platform.html', context)


def section(request, plataforma, secao):
    current_platform = get_platform(plataforma)
    if current_platform is None:
        raise Http404('Plataforma não encontrada')

    current_section = get_section(current_platform, secao)
    if current_section is None:
        raise Http404('Seção não encontrada')

    sections = current_platform['sections']
    index = sections.index(current_section)

    context = {
        'platforms': load_catalog(),
        'platform': current_platform,
        'section': current_section,
        'previous': sections[index - 1] if index > 0 else None,
        'next': sections[index + 1] if index < len(sections) - 1 else None,
        'current': plataforma,
        'current_section': secao,
    }
    return render(request, 'apidocs/section.html', context)
