from django.conf.urls.defaults import patterns
import settings
#from django.views.static import serve                                           #Necessary @UnusedImport
#from django.conf import settings

urlpatterns = patterns('',
    
    (r'^$', 'realtime.views.home'),
    (r'^realtime$', 'realtime.views.realtime'),
    (r'^second$', 'realtime.views.second'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
