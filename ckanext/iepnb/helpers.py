from ckan.common import json, config
from ckan.lib.plugins import DefaultTranslation
from ckan.lib import helpers as ckan_helpers
import ckanext.iepnb.config as iepnb_config
from ckanext.iepnb.utils import get_facets_dict
from urllib.request import urlopen
import ckan.logic as logic
import logging


logger = logging.getLogger(__name__)
all_helpers = {}

def helper(fn):
    """
    collect helper functions into ckanext.scheming.all_helpers dict
    """
    all_helpers[fn.__name__] = fn
    return fn

@helper
def iepnb_default_facet_search_operator():
    '''Returns the default facet search operator: AND/OR 
    '''
    facet_operator = iepnb_config.default_facet_operator #config.get('ckanext.dge.facet.default.search.operator', 'AND')
    if facet_operator and (facet_operator.upper() == 'AND' or facet_operator.upper() == 'OR'):
        facet_operator = facet_operator.upper()
    else:
        facet_operator = 'AND'
    return facet_operator

@helper
def iepnb_decode_json(cadena):
    """Convierte un texto json en un objeto phyton
    """
    objeto=json.loads(cadena)
    #objeto=cadena    
    return objeto

@helper
def iepnb_breadcrumbs(lang = ''):
    """'Devuelve un texto con el json que contiene las migas de pan.
    Si puede, lo obtiene dinámicamente del servidor iepnb.home, con la ruta path_breadcrumbs.
    Si la ruta no está definida, toma por defecto el valor indicado en iepnb.breadcrumbs
    """
    
    if iepnb_config.path_breadcrumbs == '':
        return iepnb_config.breadcrumbs
    else:
        breadcrumbs_url = iepnb_config.server_menu
        if lang == '' or lang =='es':
            breadcrumbs_url += path_breadcrumbs
        else:
            breadcrumbs_url += ('/'+lang+path_breadcrumbs)
            
        logger.debug(u'breadcrumbs_url {0}'.format(iepnb_config.menu_url))
        
        breadcrumbs_page=urlopen(breadcrumbs_url, context=gcontext)
        breadcrumbs_text_bytes = breadcrumbs_page.read()
        breadcrumbs_text = breadcrumbs_text_bytes.decode("utf-8")
        
        return breadcrumbs_text

@helper        
def iepnb_get_facet_class(name,item):
    respuesta=""
    if name=="theme":
        respuesta=item.split('/')[-1].lower()
    elif name=="theme_es":
        respuesta=respuesta=item.split('/')[-1].lower()
        
    return respuesta


@helper        
def iepnb_home():
    """Devuelve el servidor donde está instalado ckan, configurado en ckan.site_url
    """
    return iepnb_config.server_menu

@helper
def iepnb_locale_default():
    """DEvuelve el locale_default de la configuración
    """
    
    return iepnb_config.locale_default

@helper    
def iepnb_popular_tags():
    """Devuelve el número de etiquetas populares que se mostrarán, según iepnb.populat_tags
    """
    
    return iepnb_config.popular_tags

@helper
def iepnb_menu(lang = ''):
    """Busca el texto json con la descripción del menú en iepnb.server
    """
    menu_url=iepnb_config.server_menu
    if lang == '' or lang =='es':
        menu_url += iepnb_config.path_menu
    else:
        menu_url += ('/'+lang+path_menu)
        
    logger.debug(u'menu_url: {0}'.format(menu_url))
        
    menu_page=urlopen(menu_url, context=iepnb_config.gcontext)
    logger.debug(u'menu_url open')
    menu_text_bytes = menu_page.read()
    logger.debug(u'menu_url received')
    menu_text = menu_text_bytes.decode("utf-8")
    
    
    return menu_text
    #return 'https://iepnb-des.tragsatec.es'
    
@helper      
def iepnb_to_url_segment(cadena):
    """Obsolete: convierte un literal de nombre de página en un segmento de url según Drupal
    """
    
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )
    _lcadena = cadena.strip().lower()
    for a, b in replacements:
        _lcadena = _lcadena.replace(a, b)
    _lcadena = _lcadena.replace(" ","-")
    return _lcadena

@helper
def iepnb_organization_name(item):
    respuesta=item['display_name']
    try:
        org_dic = ckan_helpers.get_organization(item['display_name'])
        if org_dic is not None:
            respuesta=org_dic['name']
        else:
            logger.warning('No se ha podido encontrar el nombre de la organización con id %'.format(item['display_name']))
    except Exception as e:
        logger.error("Excepción al intentar encontrar el nombre de la organización: %".format(e))
    return respuesta

@helper
def iepnb_get_facet_label(facet):    
    return get_facets_dict[facet]
    
