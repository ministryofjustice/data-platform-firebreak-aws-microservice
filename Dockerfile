FROM python:3.11

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app


# Use a non-root user
RUN addgroup --gid 31337 --system appuser \
  && adduser --uid 31337 --system appuser --ingroup appuser
RUN chown --recursive appuser:appuser /code
USER 31337

#
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "80"]
