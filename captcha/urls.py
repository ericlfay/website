from django.conf.urls import url
from .views import loginview

urlpatterns = [
    url(r'login/$', loginview),
    url(r'^account/signup/$', SignUpValidatedView.as_view()),
]
