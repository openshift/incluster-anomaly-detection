FROM registry.access.redhat.com/ubi8/python-39

LABEL name="incluster-anomaly-poc" \
      description="Anomaly test docker file" \
      target-file="Dockerfile"

RUN pip install --upgrade --no-cache-dir pip && \
    pip install --upgrade --no-cache-dir pipenv

WORKDIR /opt/app-root/
COPY ./Pipfile* /opt/app-root/

RUN PIPENV_VENV_IN_PROJECT=1 PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --system --deploy --ignore-pipfile

COPY src /opt/app-root/src