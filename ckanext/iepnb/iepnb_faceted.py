from abc import ABC
import ckan.plugins as plugins
from ckan.common import request, config
import ckanext.iepnb.config as iepnb_config

class IepnbFaceted():
    plugins.implements(plugins.IFacets)
    facet_list=[]
    
    def facet_load_config(self,facet_list):
        self.facet_list= facet_list
    
    #Remove group facet
    def _facets(self, facets_dict):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        
        #facetas=config.get('iepnb.facets', '').split()
        lang_code = request.environ['CKAN_LANG']
        facets_dict.clear()
        for facet in self.facet_list:
            facets_dict[facet] = plugins.toolkit._(iepnb_config.facets_dict[facet])
        
        #tag_key = 'tags_' + lang_code
        #facets_dict[tag_key] = plugins.toolkit._('Tag')
        # FIXME: PARA FACETA COMUN DE TAGS
        return self._facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        
        return facets_dict

    def organization_facets(self, facets_dict, organization_type, package_type):

        #lang_code = pylons.request.environ['CKAN_LANG']
        #facets_dict.clear()

        #facets_dict['organization'] = plugins.toolkit._('Organization')
        #facets_dict['theme_id'] =  plugins.toolkit._('Category')
        #facets_dict['res_format_label'] = plugins.toolkit._('Format')
        #facets_dict['publisher_display_name'] = plugins.toolkit._('Publisher')
        #facets_dict['administration_level'] = plugins.toolkit._('Administration level')
        #facets_dict['frequency'] = plugins.toolkit._('Update frequency')
        #tag_key = 'tags_' + lang_code
        #facets_dict[tag_key] = plugins.toolkit._('Tag')
        # FIXME: PARA FACETA COMUN DE TAGS
        # facets_dict['tags'] = plugins.toolkit._('Tag')
        #return self._facets(facets_dict)
        return facets_dict

