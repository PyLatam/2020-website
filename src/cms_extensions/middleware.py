# -*- coding: utf-8 -*-
import datetime

from django.utils import translation
from django.conf import settings

from cms.utils.compat.dj import MiddlewareMixin


class LanguageCookieMiddleware(MiddlewareMixin):

    def process_request(self, request):
        language = translation.get_language()
        request_language = translation.get_language_from_request(request, check_path=True)
        # request language fallsback to session,
        # then cookies and last to accept-headers
        # this might not match the thread language
        set_session = request_language != language

        if set_session:
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            request.session.save()

    def process_response(self, request, response):
        language = translation.get_language()

        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES and \
                request.COOKIES[settings.LANGUAGE_COOKIE_NAME] == language:
            return response
        max_age = 365 * 24 * 60 * 60  # 10 years
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, expires=expires)
        return response
