FROM python:3
ADD ./web /srv
WORKDIR /srv
RUN pip install -r requirements.txt
CMD ["python3", "pyapp.py"]

# FROM registry.fedoraproject.org/fedora-minimal:latest
# RUN microdnf -y install python3-flask python3-pip python3-devel postgresql-devel gcc && microdnf clean all
# ADD ./web /srv
# WORKDIR /srv
# RUN pip3 install -r requirements.txt
# CMD ["python3", "pyapp.py"]