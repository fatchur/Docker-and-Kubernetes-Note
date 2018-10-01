FROM nvidia/cuda:8.0-devel-ubuntu16.04
LABEL maintainer "ULSEE inc. <collin@ulsee.com>"
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl && \
    rm -rf /var/lib/apt/lists/*

RUN echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list

ENV CUDNN_VERSION 6.0.21
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"

RUN apt-get update && apt-get install -y --no-install-recommends \
            libcudnn6=$CUDNN_VERSION-1+cuda8.0 \
            libcudnn6-dev=$CUDNN_VERSION-1+cuda8.0 && \
    rm -rf /var/lib/apt/lists/*

# ----------------- end of nvida cuda and cudnn

RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng12-dev libhdf5-dev
    
RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python2.7-dev python-pip 

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow-gpu==1.4.1
RUN pip3 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip3 install keras --no-deps

RUN pip2 install --upgrade pip
RUN pip2 install tensorflow-gpu==1.4.1
RUN pip2 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip2 install keras --no-deps

RUN ["mkdir", "notebooks"]
COPY jupyter_notebook_config.py /root/.jupyter/

# ------------------- opencv dependencies ------------------
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
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/Itseez/opencv/archive/3.2.0.zip && \
    unzip 3.2.0.zip && \
    rm 3.2.0.zip && \
    mv opencv-3.2.0 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \
    -DWITH_IPP=OFF \
    -DWITH_CUDA=OFF \
    -DWITH_QT=ON \ 
    -DWITH_OPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j4 && \
    make install && \ 
    ldconfig

COPY . /usr/src/app 
# ------------- end of opencv -------------------

# ------------- installing darknet ori ----------
WORKDIR /media/nodeflux/DATA/darknet
RUN cmake

# Jupyter and Tensorboard ports
EXPOSE 8888 6006

# Store notebooks in this mounted directory
VOLUME /notebooks
WORKDIR "/root"
CMD ["/bin/bash"]
