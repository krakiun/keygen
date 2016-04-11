from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from keygen import views

urlpatterns = [
    url(r'^keys/$', views.Status.as_view(), name='status'),
    url(r'^get/$', views.GetKey.as_view(), name='get_key'),
    url(r'^keys/(?P<code>[A-Za-z0-9]{4})/$', views.KeyView.as_view(), name='key_view'),
    url(r'^docs/', include('rest_framework_swagger.urls'), ),
    url(r'^$', views.index, name='homepage'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
