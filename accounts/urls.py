from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.loginview, name='login'),
    url(r'^logout/', views.logout_view, name='logout'),
    url(r'^(?P<user>[0-9]+)/', views.user_detail, name='report_detail'),
    url(r'^sub/(?P<user>[0-9]+)/', views.all_user_subs, name='user_sub_detail'),
]