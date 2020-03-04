FROM python:3.7.6-stretch

COPY . /scripts/
WORKDIR /scripts

# install dependencies
RUN apt-get update && apt-get install -y \
  wget 
RUN apt-get install -y python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgtk2.0-de
    
# ------------------- opencv dependencies ------------------
ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

# Various Python and C/build deps
RUN apt-get update && apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    unzip \ 
    pkg-config \
    python-dev \ 
    python-opencv \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev

RUN apt-get install -y \
    libpng-dev \ 
    libtiff-dev \  
    libgtk2.0-dev \ 
    python-numpy \ 
    python-pycurl \ 
    libatlas-base-dev \
    gfortran \
    webp \ 
    python-opencv \ 
    qt5-default \
    libvtk6-dev \ 
    zlib1g-dev

#RUN add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
#RUN apt update
#RUN apt install libjasper-dev

#------------ Install Open CV - Warning, this takes absolutely forever
WORKDIR /
RUN pwd
RUN wget https://github.com/Itseez/opencv/archive/3.4.2.zip -O opencv.zip \
	&& unzip /opencv.zip \
	&& wget https://github.com/Itseez/opencv_contrib/archive/3.4.2.zip -O opencv_contrib.zip \
	&& unzip /opencv_contrib \
	&& mkdir opencv-3.4.2/cmake_binary \
	&& cd opencv-3.4.2/cmake_binary \
	&& apt-get update \
	&& cmake -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.4.2/modules \
	  -DWITH_IPP=OFF \
          -DWITH_CUDA=OFF \
          -DWITH_QT=ON \ 
          -DWITH_OPENGL=ON \ 
          -DFORCE_VTK=ON \
          -DWITH_TBB=ON \
          -DWITH_GDAL=ON \
          -DWITH_XINE=ON \
          -DBUILD_EXAMPLES=ON .. \
	&& make -j8 \
	&& make install \
	&& rm /opencv.zip \
	&& rm /opencv_contrib.zip \
	&& rm -r /opencv-3.4.2 \
	&& rm -r /opencv_contrib-3.4.2

COPY . /usr/src/app 
# ------------- end of opencv -------------------

WORKDIR /home
EXPOSE 8001
CMD ["python3", "main.py", "2> /dev/null"]
