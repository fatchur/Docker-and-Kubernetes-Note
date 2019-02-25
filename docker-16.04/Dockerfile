FROM nvidia/cuda:9.0-base-ubuntu16.04

LABEL maintainer="Craig Citro <craigcitro@google.com>"

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cuda-command-line-tools-9-0 \
        cuda-cublas-dev-9-0 \
        cuda-cudart-dev-9-0 \
        cuda-cufft-dev-9-0 \
        cuda-curand-dev-9-0 \
        cuda-cusolver-dev-9-0 \
        cuda-cusparse-dev-9-0 \
        curl \
        git \
        libcudnn7=7.2.1.38-1+cuda9.0 \
        libcudnn7-dev=7.2.1.38-1+cuda9.0 \
        libcurl3-dev \
        libfreetype6-dev \
        libhdf5-serial-dev \
        libpng12-dev \
        libzmq3-dev \
        pkg-config \
        python-dev \
        rsync \
        software-properties-common \
        unzip \
        zip \
        zlib1g-dev \
        wget \
        && \
    rm -rf /var/lib/apt/lists/* && \
    find /usr/local/cuda-9.0/lib64/ -type f -name 'lib*_static.a' -not -name 'libcudart_static.a' -delete && \
    rm /usr/lib/x86_64-linux-gnu/libcudnn_static_v7.a

# ----------------- end of nvida cuda and cudnn

RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng12-dev libhdf5-dev
    
RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python2.7-dev python-pip 

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow-gpu==1.12
RUN pip3 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip3 install keras --no-deps
RUN pip3 install flask
RUN pip3 install mysql-connector
RUN pip3 install statsmodels
RUN pip3 install gunicorn
RUN pip3 install request
RUN pip3 install imutils
RUN python3 -m pip install ipykernel
RUN python3 -m ipykernel install --user

RUN pip2 install --upgrade pip
RUN pip2 install tensorflow-gpu==1.12
RUN pip2 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip2 install keras --no-deps
RUN pip2 install flask
RUN pip2 install mysql-connector
RUN pip2 install statsmodels
RUN pip2 install request
RUN pip2 install imutils
RUN pip2 install gunicorn


### Optional package from my repository
WORKDIR /
RUN git clone https://github.com/fatchur/Simple-Tensor.git
WORKDIR /Simple-Tensor
RUN python3 setup.py install
RUN python2 setup.py install

WORKDIR /
RUN git clone https://github.com/fatchur/Feature-Engineering-Utils.git
WORKDIR /Feature-Engineering-Utils
RUN python3 setup.py install
RUN python2 setup.py install

WORKDIR /
RUN git clone https://github.com/fatchur/Mysql-Utils.git
WORKDIR /Mysql-Utils
RUN python3 setup.py install 
RUN python2 setup.py install

WORKDIR /
RUN git clone https://github.com/fatchur/COMDUTILS-computer-vision-deployment-utils.git
WORKDIR /COMDUTILS-computer-vision-deployment-utils
RUN python3 setup.py install 
RUN python2 setup.py install
###### ----------------------------------------------------


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
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \ 
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

# Jupyter and Tensorboard ports
EXPOSE 8888 6006

# Store notebooks in this mounted directory
WORKDIR "/root"
CMD ["/bin/bash"]
