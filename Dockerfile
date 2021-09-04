FROM python:3.8-slim-buster
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./turbofan_dashboard /turbofan_dashboard

WORKDIR /turbofan_dashboard

EXPOSE 8501
CMD ["streamlit", "run", "dashboard.py"]
