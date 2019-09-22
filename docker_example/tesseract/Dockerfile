FROM ubuntu:18.04

RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng-dev libhdf5-dev

RUN pip3 install --upgrade pip
RUN apt-get update

RUN apt-get install -y tesseract-ocr-ind
RUN apt-get update

# ------------------- opencv dependencies ------------------
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update
RUN apt-get install -y \ 
    build-essential \  
    pkg-config \
    libavcodec-dev \
    python-dev \  
    libopencv-dev \ 
    libjpeg-dev \ 
    libavformat-dev \
    libswscale-dev \
    libpng-dev \ 
    libtiff-dev \ 
    libdc1394-22-dev \
    libgtk2.0-dev 

RUN apt-get update


#------------ Install Open CV - Warning, this takes absolutely forever
RUN apt-get update
WORKDIR /app
COPY . /app
RUN pip3 install --trusted-host pypi.python.org -r /app/requirements.txt
EXPOSE 8080
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8080", "--timeout", "7000"]
