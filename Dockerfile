FROM python:3.8.12-slim-buster

EXPOSE 5000



COPY test.py /test.py
COPY utils.py /utils.py
COPY requirements.txt /requirements.txt


RUN pip install -r requirements.txt


CMD streamlit run test.py --server.port=$PORT

