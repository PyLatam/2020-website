# <WARNING>
# Everything within sections like <TAG> is generated and can
# be automatically replaced on deployment. You can disable
# this functionality by simply removing the wrapping tags.
# </WARNING>

# <DOCKER_FROM>
FROM divio/base:4.15-py3.6-slim-stretch
# </DOCKER_FROM>
RUN apt update && curl -sL https://deb.nodesource.com/setup_10.x| bash\
          && apt-get install -y nodejs\
          && rm -rf /var/lib/apt/lists/*
# <NPM>
# package.json is put into / so that mounting /app for local
# development does not require re-running npm install
ENV PATH=/node_modules/.bin:$PATH
COPY package.json /
RUN (cd / && npm install --production && rm -rf /tmp/*)
# </NPM>

# <BOWER>
# </BOWER>

# we want to keep project-specific sources in the "src" folder
ENV PYTHONPATH=/app/src:$PYTHONPATH

# <PYTHON>
ENV PIP_INDEX_URL=${PIP_INDEX_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/+simple/} \
    WHEELSPROXY_URL=${WHEELSPROXY_URL:-https://wheels.aldryn.net/v1/aldryn-extras+pypi/${WHEELS_PLATFORM:-aldryn-baseproject-py3}/}
COPY requirements.* /app/
COPY addons-dev /app/addons-dev/
RUN pip-reqs compile && \
    pip-reqs resolve && \
    pip install \
        --no-index --no-deps \
        --requirement requirements.urls
# </PYTHON>

# This app is automatically installed by the aldryn-django-cms package.
# There are legacy reasons for this but in this case we cna just remove it.
# Can't leave it in because both this and django-recaptcha have a captcha package :/
RUN pip uninstall --yes django-simple-captcha && pip install django-recaptcha==2.0.2

# <SOURCE>
COPY . /app
# </SOURCE>

# <GULP>
# </GULP>

RUN rm -rf /static/*

# <STATIC>
RUN DJANGO_MODE=build python manage.py collectstatic --noinput
# </STATIC>
