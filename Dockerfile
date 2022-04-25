FROM ubuntu
RUN apt-get update
RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip install paramiko
RUN pip install apache-log-parser
RUN pip install dash
RUN pip install pandas
COPY ./ /projet
EXPOSE 8050
ENTRYPOINT ["python3", "/projet/interface.py"]

