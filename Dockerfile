FROM cpa_base
USER user
COPY . /usr/src/app/
RUN ./manage.py bower install --settings=web.settings.base
