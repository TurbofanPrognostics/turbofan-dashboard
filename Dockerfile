FROM samdobson/streamlit:latest
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./turbofan_dashboard .
