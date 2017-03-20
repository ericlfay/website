from django.conf.urls import url
from .views import loginview

urlpatterns = [
    url(r'login/$', loginview),
]
