FROM tiangolo/uwsgi-nginx-flask:python3.6
WORKDIR /var/www
COPY requirement.txt .
RUN pip install -r /var/www/requirement.txt
COPY . ./
#CMD ["export", "FLASK_APP=flaskr"]
#CMD ["export", "FLASK_ENV=development"]
ENV FLASK_APP=flaskr
ENV FLASK_ENV=development
#CMD ['flask', 'run', '--host=0.0.0.0']
CMD exec flask run --host=0.0.0.0
