from django.conf.urls import url
from . import views
app_name = 'subnetworks'

urlpatterns = [
    url(r'^subs/', views.all_subs, name="all_subs"),
    url(r'^(?P<sub_name>\w+)/$', views.sub, name='sub_name'),
    url(r'^(?P<pk>[0-9]+)/follow', views.follow, name='follow'),
]
