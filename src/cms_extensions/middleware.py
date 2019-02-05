# -*- coding: utf-8 -*-
import datetime

from django.utils.translation import LANGUAGE_SESSION_KEY, get_language
from django.conf import settings

from cms.utils.compat.dj import MiddlewareMixin


class LanguageCookieMiddleware(MiddlewareMixin):

    def process_request(self, request):
        language = get_language()
        cookie_language = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        session_language = request.session.get(LANGUAGE_SESSION_KEY)

        if session_language:
            set_session = session_language == language
        else:
            set_session = cookie_language and cookie_language != language

        if set_session:
            request.session[LANGUAGE_SESSION_KEY] = language
            request.session.save()

    def process_response(self, request, response):
        language = get_language()

        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES and \
                request.COOKIES[settings.LANGUAGE_COOKIE_NAME] == language:
            return response
        max_age = 365 * 24 * 60 * 60  # 10 years
        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language, expires=expires)
        return response
