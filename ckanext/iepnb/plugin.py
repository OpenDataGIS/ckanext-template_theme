import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import json

def decode_json(cadena):
    objeto=json.loads(cadena)
    #objeto=cadena    
    return objeto

def get_home():
    return 'https://iepnb-des.tragsatec.es'

def get_path():
    return 'Nuestros datos, Catálogo de datos'

def to_url_segment(cadena):
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
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic',
            'iepnb')
        iepnb = type('', (), {})()
        iepnb.home='https://iepnb-des.tragsatec.es'
        iepnb.ckan=type('', (), {})()
        iepnb.ckan.path='nuestros-datos/catalogo-de-datos'
        #toolkit.g.set_app_global('iepnb.home','https://iepnb-des.tragsatec.es')
    def get_helpers(self):
        return {'iepnb_decode_json': decode_json,
                'iepnb_home': get_home,
                'iepnb_path': get_path,
                'iepnb_to_url_segment': to_url_segment}
