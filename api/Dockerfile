FROM python:3.6-slim
LABEL maintainer="balantgnanam@gmail.com"


COPY requirements.txt ./requirements.txt
WORKDIR ./

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt \
  && pip install --upgrade pip \
  && pip install --upgrade setuptools \
  && pip install -U pip setuptools wheel \
  && pip install -U spacy \
  && python -m spacy download en_core_web_sm

RUN pip install -U waitress

COPY . ./

EXPOSE 5002
ENTRYPOINT ["python"]
CMD ["app/runserver.py"]
