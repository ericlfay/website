# coding:utf-8
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
from django.views.generic import View

from allauth.account.views import SignupView
from captcha.geetest import GeetestLib


# Create your views here.
captcha_id = "a37c8a215b48279cdb65f10961af2bad"
private_key = "233548502f29536550efec5a007451e2"


class CaptchaView(View):
	'''验证view'''
    captcha_lib = GeetestLib(captcha_id, private_key)

    def get(self, request):
        self._add_captcha_to_session()
        return HttpResponse(self._get_captcha())

    def _get_captcha(self):
        return self.captcha_lib.get_response_str()

    def _add_captcha_to_session(self):
        user_id = self.request.user.id
        status = self.captcha_lib.pre_process(user_id)
        self.request.session[self.captcha_lib.GT_STATUS_SESSION_KEY] = status
        self.request.session['user_id'] = user_id


class CaptchaValidateMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.request = request

        # 如果提交表单时, 验证码验证失败, 重定向回当前地址
        if request.method == 'POST' and not self._validate_captcha():
            return redirect(request.path)
        return super(CaptchaValidateMixin, self).dispatch(request,
                                                          *args,
                                                          **kwargs)

    def _validate_captcha(self):
        post_data = self.request.POST
        session = self.request.session

        captcha_lib = GeetestLib(settings.CAPTCHA_ID, settings.CAPTCHA_KEY)
        challenge = post_data.get(captcha_lib.FN_CHALLENGE, '')
        validate = post_data.get(captcha_lib.FN_VALIDATE, '')
        seccode = post_data.get(captcha_lib.FN_SECCODE, '')
        captcha_server_status = session.get(captcha_lib.GT_STATUS_SESSION_KEY,
                                            '')
        user_id = session.get('user_id', None)

        if captcha_server_status:
            # 如果验证码服务器正常, 在验证码服务器上验证
            result = captcha_lib.success_validate(challenge, validate,
                                                  seccode, user_id)
        else:
            # 如果验证码服务器宕机, 在本地验证
            result = captcha_lib.failback_validate(challenge, validate,
                                                   seccode)
        return result


class SignUpValidatedView(CaptchaValidateMixin, SignupView):
    pass
