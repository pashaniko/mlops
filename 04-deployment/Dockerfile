FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

RUN pip install -U pip 
RUN pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]
RUN pipenv install --system --deploy

RUN mkdir ./output
COPY [ "homework.py", "homework.py" ]

ENTRYPOINT [ "python", "homework.py", "2023", "5" ]