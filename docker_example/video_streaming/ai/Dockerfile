FROM tensorflow/tensorflow:1.12.0-devel-gpu-py3

COPY requirements.txt /scripts/
WORKDIR /scripts

# install dependencies
RUN apt-get update && apt-get install -y \
  wget 
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgtk2.0-dev

WORKDIR /home
EXPOSE 8002
CMD ["python3", "main.py"] 

