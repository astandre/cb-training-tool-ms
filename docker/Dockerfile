FROM python:3.7

RUN pip install gunicorn

COPY docker/settings.ini /app/kbsbot/training_tool/settings.ini

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

WORKDIR /app/kbsbot/training_tool

EXPOSE 8007
CMD ["gunicorn", "-b", "0.0.0.0:8007", "run:app"]


