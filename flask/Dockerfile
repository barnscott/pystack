FROM python:3
ADD ./web /srv
WORKDIR /srv
RUN pip install -r requirements.txt
CMD ["python3", "pyapp.py"]