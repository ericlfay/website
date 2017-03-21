from django.conf.urls import url
from .views import CaptchaView, SignUpValidatedView


urlpatterns = [
    url(r'^captcha/$', CaptchaView.as_view(),
        name='get_captcha'),
    url(r'^account/signup/$', SignUpValidatedView.as_view()),
]
