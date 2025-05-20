FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UV_SYSTEM_PYTHON 1

WORKDIR /backend

RUN pip install uv

COPY pyproject.toml .
COPY uv.lock .

RUN uv pip install --system --no-cache -r pyproject.toml

COPY ./ /backend/

# Port setup
ENV PORT 8000
EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]