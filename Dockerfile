FROM python:3.12-alpine

WORKDIR /app

COPY scripts/dashboard_app.py /app/dashboard_app.py

ENV PORT=8500
ENV DATA_DIR=/data

EXPOSE 8500

CMD ["python3", "/app/dashboard_app.py"]
