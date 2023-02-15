import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import logging
from ckan.common import json, config
from urllib.request import urlopen
import ssl

logger = logging.getLogger(__name__)

#migas de pan por defecto definidas en el fichero de configuración con iepnb.breadcrumbs
breadcrumbs=""

#servidor al que se ha de solicitar el objeto json con el menú y las migas de pan
server_menu=""

#path dentro del servidor para solicitar el menu. Va separado para poder intercalar el prefijo de idioma
#se define en el menú ini con epnb.path_menu
path_menu=""

#Ruta a la descarga de migas de pan del servidor definida en el fichero de configuración con iepnb.path.breadcrumbs 
path_breadcrumbs=""

#número de etiquetas populares para mostrar en la página principal
popular_tags=0


def decode_json(cadena):
    """Convierte un texto json en un objeto phyton
    """
    objeto=json.loads(cadena)
    #objeto=cadena    
    return objeto

def get_breadcrumbs(lang = ''):
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
        
def get_home():
    """Devuelve el servidor donde está instalado ckan, configurado en ckan.site_url
    """
    return server_menu

def get_locale_default():
    """DEvuelve el locale_default de la configuración
    """
    
    return config.get('ckan.locale_default', '')
    
def get_popular_tags():
    """Devuelve el número de etiquetas populares que se mostrarán, según iepnb.populat_tags
    """
    
    return popular_tags

def get_menu(lang = ''):
    """Busca el texto json con la descripción del menú en iepnb.server
    """
    menu_url=server_menu
    if lang == '' or lang =='es':
        menu_url += path_menu
    else:
        menu_url += ('/'+lang+path_menu)
        
    logger.debug(u'menu_url {0}'.format(menu_url))
    
    menu_page=urlopen(menu_url, context=gcontext)
    menu_text_bytes = menu_page.read()
    menu_text = menu_text_bytes.decode("utf-8")
    
    
    return menu_text
    #return 'https://iepnb-des.tragsatec.es'
    
      
def to_url_segment(cadena):
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
    

class IepnbPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        global breadcrumbs
        global gcontext
        global path_breadcrumbs
        global path_menu
        global popular_tags
        global server_menu

        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'iepnb')
        toolkit.add_resource('assets', 'ckanext-iepnb')
       
        server_menu = config.get('iepnb.server', 'https://iepnb-des.tragsatec.es')
        path_menu = config.get('iepnb.path_menu', '/api/menu_items/main')
        breadcrumbs = config.get('iepnb.breadcrumbs', '')
        popular_tags= toolkit.asint(config.get('iepnb.popular_tags', 3))
        #if breadcrumbs != '':
        #    breadcrumbs = json.loads(breadcrumbs)
        path_breadcrumbs = config.get('iepnb.path_breadcrumbs', '')
        gcontext = ssl.SSLContext()
        


    def get_helpers(self):
        return { 'iepnb_decode_json': decode_json,
            'iepnb_breadcrumbs': get_breadcrumbs,
            'iepnb_home': get_home,
            'iepnb_locale_default' : get_locale_default,
            'iepnb_menu': get_menu,
            'iepnb_popular_tags': get_popular_tags,
            'iepnb_to_url_segment': to_url_segment}
