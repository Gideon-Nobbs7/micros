FROM python:3.12 AS build

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --prefix=/app/install -r requirements.txt

FROM build as development

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY --from=build /app/install /usrr/local

COPY . /app

CMD ["python", "main.py"]


FROM build as production

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN useradd -r nduser

# RUN --mount=type=cache,target=/root/.cache/pip \
#     pip install --no-cache-dir -r /app/requirements.txt

COPY --from=build /app/install /usr/local

# Copy files and switch ownership to non-root user
COPY --chown=nduser . /app

# Set permissions while being a root user
RUN chmod -RR 755 /app

# Switch to a non-root user
USER nduser

CMD [ "python", "main.py" ]

