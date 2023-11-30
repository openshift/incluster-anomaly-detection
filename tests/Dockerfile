FROM registry.access.redhat.com/ubi8/python-39

LABEL name="incluster-anomaly-ci" \
      description="Anomaly detection CI docker file" \
      target-file="Dockerfile"

# Install pip & pipenv
RUN pip install --upgrade --no-cache-dir pip && \
    pip install --upgrade --no-cache-dir pipenv

# Setup work directory
WORKDIR /opt/app-root/

# Copy files to workdir
COPY ./Pipfile* /opt/app-root/
COPY ./setup.cfg /opt/app-root/setup.cfg

# Install pipenv
RUN PIPENV_VENV_IN_PROJECT=1 PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --dev --system --deploy --ignore-pipfile

# Copy files to workdir
COPY /src /opt/app-root/src
COPY /tests /opt/app-root/tests