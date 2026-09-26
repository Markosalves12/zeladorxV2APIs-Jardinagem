import json
from functools import lru_cache
from pathlib import Path


# ============================================================
# CATÁLOGO DA DOCUMENTAÇÃO
# ============================================================
#
# O arquivo data/catalog.json é gerado a partir dos cadernos
# Jupyter dos repositórios de documentação:
#
# - apis-jardinagem-zeladorx
# - zeladorxV2APIs-LimpezaPredial
# - zeladorxV2APIs-specials
#
# Senhas, usuários e tokens são substituídos por exemplos.

CATALOG_PATH = Path(__file__).resolve().parent / 'data' / 'catalog.json'

SECTION_ICONS = {
    'auth': 'fa-key',
    'empresa-primaria': 'fa-building',
    'empresas-secundarias': 'fa-city',
    'unidades': 'fa-location-dot',
    'localidade': 'fa-map-location-dot',
    'areas': 'fa-draw-polygon',
    'terrenos': 'fa-mountain-sun',
    'vegetacao': 'fa-leaf',
    'catalogo-servicos': 'fa-book-open',
    'gerentes': 'fa-user-tie',
    'servicos-configurados': 'fa-sliders',
    'servicos-agendados': 'fa-calendar-days',
    'servicos-realizados': 'fa-circle-check',
    'checklist': 'fa-list-check',
    'permissoes-usuario': 'fa-user-shield',
    'codigos-de-permissao': 'fa-hashtag',
    'configuracoes-de-usuario': 'fa-user-gear',
}


@lru_cache(maxsize=1)
def load_catalog():
    with open(CATALOG_PATH, encoding='utf-8') as file:
        platforms = json.load(file)

    for platform in platforms:
        for section in platform['sections']:
            section['icon'] = SECTION_ICONS.get(section['slug'], 'fa-code')

    return platforms


def get_platform(slug):
    return next((p for p in load_catalog() if p['slug'] == slug), None)


def get_section(platform, slug):
    return next((s for s in platform['sections'] if s['slug'] == slug), None)


def get_stats():
    platforms = load_catalog()
    sections = sum(len(p['sections']) for p in platforms)
    endpoints = sum(len(s['endpoints']) for p in platforms for s in p['sections'])
    return {'platforms': len(platforms), 'sections': sections, 'endpoints': endpoints}
