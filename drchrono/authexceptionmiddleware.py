from django.shortcuts import HttpResponse, redirect

from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social import exceptions as social_exceptions

class DrchronoSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        if not isinstance(exception, social_exceptions.SocialAuthBaseException):
            return redirect('/')
        print '---------in middleware---------'
        if type(exception) == social_exceptions.AuthCanceled or \
            type(exception) == social_exceptions.AuthFailed:
            return redirect('/')
        # elif type(exception) == social_exceptions.AuthFailed:
        #     return HttpResponse("I'm the Apple %s" % exception)
        else:
            return HttpResponse('I do not know what happened! But Drchrono says %s' % exception)