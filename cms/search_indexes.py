from haystack import indexes
from cms.models.pagemodel import Page
from cms.models.pluginmodel import CMSPlugin
from cms.models.titlemodels import Title
import datetime

class PageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=False)
    title = indexes.CharField()
    tags = indexes.CharField()
    pagecontent = indexes.CharField()
    
    # Not in template but used for filtering
    url = indexes.CharField(model_attr='get_absolute_url')
    limit_visibility = indexes.IntegerField(model_attr='limit_visibility_in_menu', null=True) #Because for some reason cms initializes pages with "None"....
    pageowner = indexes.CharField(model_attr='created_by')

    # Based on http://james.lin.net.nz/2013/11/06/django-cms-haystack-2-0-search-index/ 
    def prepare(self, obj):
        self.prepared_data = super(PageIndex, self).prepare(obj)
        # Find all plugins on the page
        page_content=''
        plugins = CMSPlugin.objects.filter(placeholder__in=obj.placeholders.all())
        for plugin in plugins:
            instance, _ = plugin.get_plugin_instance()
            if hasattr(instance, 'search_fields'):
                page_content += ''.join(getattr(instance, field) for field in instance.search_fields)
        page_content += obj.get_meta_description() or u''
        page_content += obj.title_set.all()[0].title or u''
        page_content += "\n"
        page_content += ', '.join([t.title for t in obj.tags.all()])
        page_content += obj.get_meta_keywords() if hasattr(obj, 'get_meta_keywords') and obj.get_meta_keywords() else u''
        self.prepared_data['text'] = page_content
        
        if obj.limit_visibility_in_menu == None:
            self.prepared_data['limit_visibility'] = 1
                    
        # TWEAK BOOST HERE (change to '_boost' for whoosh)
        self.prepared_data['boost'] = 1+(obj.score) 
        
        return self.prepared_data   
        
    def index_queryset(self, using=None):
        return Page.objects.published().filter(publisher_is_draft=False).distinct() 
        
    def get_model(self): 
        return Page  