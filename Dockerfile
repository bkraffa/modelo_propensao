FROM python:3.9-slim
RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY "Pipfile" ./
COPY "Pipfile.lock" ./

RUN pipenv install --system --deploy

COPY ["predict.py","predict.py"]
COPY ["objetos/custom_transformer_pickle.b","objetos/custom_transformer_pickle.b"]
COPY ["objetos/modelo_rfc.b","objetos/modelo_rfc.b"]
COPY bases/ bases/

ENTRYPOINT ["python", "predict.py"]