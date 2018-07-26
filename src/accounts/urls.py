from django.conf.urls import url
from django.contrib.auth.views import logout


app_name = 'accounts'

urlpatterns = [
    url('logout/$', logout, {'next_page': '/'}, name='logout'),
]