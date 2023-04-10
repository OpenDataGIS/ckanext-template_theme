import ckan.logic as logic
import logging

logger = logging.getLogger(__name__)

_facets_dict=None


def get_facets_dict():
    global _facets_dict
    if not _facets_dict:
        _facets_dict= {}

        schema=logic.get_action('scheming_dataset_schema_show')({}, {'type': 'dataset'})

        for item in schema['dataset_fields']:
            _facets_dict[item['field_name']]=item['label']
        for item in schema['resource_fields']:
            _facets_dict[item['field_name']]=item['label']
        logger.debug("Diccionario etiquetas: {0}".format(_facets_dict))
    return _facets_dict
