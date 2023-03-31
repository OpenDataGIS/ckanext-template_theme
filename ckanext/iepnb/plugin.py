from ckanext.iepnb.iepnb_faceted import IepnbFaceted
from ckanext.iepnb.iepnb_package_controller import IepnbPackageController
import ckanext.iepnb.config as iepnb_config
import ckanext.iepnb.dge_helpers as helpers
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import json, config
from ckan.lib.plugins import DefaultTranslation
import logging
from urllib.request import urlopen
import ssl
import os

logger = logging.getLogger(__name__)
server_menu=""
path_menu=""
breadcrumbs=""
gcontext=""
path_breadcrumbs=""
popular_tags=None
proxy=None

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
    facet_operator = 'AND' #config.get('ckanext.dge.facet.default.search.operator', 'AND')
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
    
    if path_breadcrumbs == '':
        return breadcrumbs
    else:
        breadcrumbs_url = server_menu
        if lang == '' or lang =='es':
            breadcrumbs_url += path_breadcrumbs
        else:
            breadcrumbs_url += ('/'+lang+path_breadcrumbs)
            
        logger.debug(u'breadcrumbs_url {0}'.format(menu_url))
        
        breadcrumbs_page=urlopen(breadcrumbs_url, context=gcontext)
        breadcrumbs_text_bytes = breadcrumbs_page.read()
        breadcrumbs_text = breadcrumbs_text_bytes.decode("utf-8")
        
        return breadcrumbs_text

@helper        
def iepnb_home():
    """Devuelve el servidor donde está instalado ckan, configurado en ckan.site_url
    """
    return server_menu

@helper
def iepnb_locale_default():
    """DEvuelve el locale_default de la configuración
    """
    
    return config.get('ckan.locale_default', '')

@helper    
def iepnb_popular_tags():
    """Devuelve el número de etiquetas populares que se mostrarán, según iepnb.populat_tags
    """
    
    return popular_tags

@helper
def iepnb_menu(lang = ''):
    """Busca el texto json con la descripción del menú en iepnb.server
    """
    menu_url=server_menu
    if lang == '' or lang =='es':
        menu_url += path_menu
    else:
        menu_url += ('/'+lang+path_menu)
        
    logger.debug(u'menu_url: {0}'.format(menu_url))
        
    menu_page=urlopen(menu_url, context=gcontext)
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

def _get_dge_helpers():
    return {
        'dge_add_additional_facet_fields': helpers.dge_add_additional_facet_fields,
        'dge_api_swagger_url': helpers.dge_api_swagger_url,
        'dge_dataset_display_fields': helpers.dge_dataset_display_fields,
        'dge_dataset_display_frequency': helpers.dge_dataset_display_frequency,
        'dge_dataset_display_name': helpers.dge_dataset_display_name,
        'dge_dataset_field_value': helpers.dge_dataset_field_value,
        'dge_dataset_tag_field_value': helpers.dge_dataset_tag_field_value,
        'dge_dataset_tag_list_display_names': helpers.dge_dataset_tag_list_display_names,
        'dge_default_facet_search_operator': helpers.dge_default_facet_search_operator,
        'dge_default_facet_sort_by_facet': helpers.dge_default_facet_sort_by_facet,
        'dge_default_locale': helpers.dge_default_locale,
        'dge_exported_catalog_files': helpers.dge_exported_catalog_files,
        'dge_get_dataset_administration_level': helpers.dge_get_dataset_administration_level,
        'dge_get_dataset_publisher': helpers.dge_get_dataset_publisher,
        'dge_get_endpoints_menu': helpers.dge_get_endpoints_menu,
        'dge_get_facet_items_dict': helpers.dge_get_facet_items_dict,
        'dge_get_organization_administration_level_code': helpers.dge_get_organization_administration_level_code,
        'dge_get_show_sort_facet': helpers.dge_get_show_sort_facet,
        'dge_harvest_frequencies': helpers.dge_harvest_frequencies,
        'dge_is_downloadable_resource': helpers.dge_is_downloadable_resource,
        'dge_list_reduce_resource_format_label': helpers.dge_list_reduce_resource_format_label,
        'dge_list_themes': helpers.dge_list_themes,
        'dge_package_list_for_source': helpers.dge_package_list_for_source,
        'dge_parse_datetime': helpers.dge_parse_datetime,
        'dge_render_datetime': helpers.dge_render_datetime,
        'dge_resource_display_name': helpers.dge_resource_display_name,
        'dge_resource_display_name_or_desc': helpers.dge_resource_display_name_or_desc,
        'dge_resource_format_label': helpers.dge_resource_format_label,
        'dge_sort_alphabetically_resources': helpers.dge_sort_alphabetically_resources,
        'dge_sparql_yasgui_doc_url': helpers.dge_sparql_yasgui_doc_url,
        'dge_sparql_yasgui_endpoint': helpers.dge_sparql_yasgui_endpoint,
        'dge_swagger_doc_url': helpers.dge_swagger_doc_url,
        'dge_tag_link': helpers.dge_tag_link,
        'dge_searched_facet_item_filter': helpers.dge_searched_facet_item_filter,
        'dge_theme_id': helpers.dge_theme_id,
        'dge_url_for_user_organization': helpers.dge_url_for_user_organization,
    }
    

class IepnbPlugin(plugins.SingletonPlugin,IepnbFaceted,IepnbPackageController, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.IPackageController)
    plugins.implements(plugins.ITranslation)


    # IConfigurer

    def update_config(self, config_):
        global breadcrumbs
        global gcontext
        global path_breadcrumbs
        global path_menu
        global popular_tags
        global server_menu
        global proxy
        
        logger.debug('Doing config...')

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'iepnb')
        toolkit.add_resource('assets', 'ckanext-iepnb')
        toolkit.add_template_directory(config, 'templates')
              
        server_menu = config.get('iepnb.server', iepnb_config.server_menu)
        path_menu = config.get('iepnb.path_menu', iepnb_config.path_menu)
        breadcrumbs = config.get('iepnb.breadcrumbs', '')
        proxy = config.get('iepnb.proxy', '')
        popular_tags= toolkit.asint(config.get('iepnb.popular_tags', 3))
        self.facet_load_config(config.get('iepnb.facet_list', '').split())
        self.package_controller_config(config.get('iepnb.default_facet_operator', iepnb_config.default_facet_operator))
        #self.package_controller_config('OR')
        #if breadcrumbs != '':
        #    breadcrumbs = json.loads(breadcrumbs)
        path_breadcrumbs = config.get('iepnb.path_breadcrumbs', '')
        gcontext = ssl.SSLContext()
        
    def get_helpers(self):
        logger.debug('Getting helpers...')
        #respuesta= _get_dge_helpers().copy()
        #respuesta.update(dict(all_helpers))
        respuesta=dict(all_helpers)
        #respuesta.update({ 
        #    'iepnb_decode_json': decode_json,
        #    'iepnb_breadcrumbs': get_breadcrumbs,
        #    'iepnb_home': get_home,
        #    'iepnb_locale_default' : get_locale_default,
        #    'iepnb_menu': get_menu,
        #    'iepnb_popular_tags': get_popular_tags,
        #    'iepnb_to_url_segment': to_url_segment,
        #    'iepnb_default_facet_search_operator': default_facet_search_operator}
        #    )
        return respuesta
    
        
    
    
    
    
