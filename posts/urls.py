from django.conf.urls import url
from . import views
app_name = 'posts'

urlpatterns = [
    url(r'^create/', views.create_report, name='create_report'),
    url(r'^(?P<pk>[0-9]+)/([-\w]+)/$', views.report_detail, name='report_detail'),
]
