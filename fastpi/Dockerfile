FROM python:3.12 AS build

WORKDIR /app

COPY requirements.txt /app/requirements.txt

FROM build as development

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app/main.py"]


FROM build as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN useradd -r nduser

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN chmod -RR 755 /app

RUN chown -R nduser:nduser /app

USER nduser

CMD [ "python", "/app/main.py" ]

