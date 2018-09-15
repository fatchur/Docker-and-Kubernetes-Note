FROM ubuntu:18.04
LABEL maintainer "NVIDIA CORPORATION <cudatools@nvidia.com>"

# CUDA 9.2 is not officially supported on ubuntu 18.04 yet, we use the ubuntu 17.10 repository for CUDA instead.
RUN apt-get update && apt-get install -y --no-install-recommends gnupg2 curl ca-certificates && \
    curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1710/x86_64/7fa2af80.pub | apt-key add - && \
    echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1710/x86_64 /" > /etc/apt/sources.list.d/cuda.list && \
    echo "deb https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/nvidia-ml.list && \
    apt-get purge --autoremove -y curl && \
    rm -rf /var/lib/apt/lists/*

ENV CUDA_VERSION 9.2.148

ENV CUDA_PKG_VERSION 9-2=$CUDA_VERSION-1
RUN apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-$CUDA_PKG_VERSION && \
    ln -s cuda-9.2 /usr/local/cuda && \
    rm -rf /var/lib/apt/lists/*

# nvidia-docker 1.0
LABEL com.nvidia.volumes.needed="nvidia_driver"
LABEL com.nvidia.cuda.version="${CUDA_VERSION}"

RUN echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf && \
    echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf

ENV PATH /usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV NVIDIA_REQUIRE_CUDA "cuda>=9.2"

###---------------- End Nvidia Docker -------------------



RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng-dev libhdf5-dev
    
RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python2.7-dev python-pip 

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow-gpu
RUN pip3 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip3 install keras --no-deps

RUN pip2 install --upgrade pip
RUN pip2 install tensorflow-gpu
RUN pip2 install numpy pandas sklearn matplotlib jupyter pyyaml h5py
RUN pip2 install keras --no-deps

## ---- Bazel
RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
  && curl https://bazel.build/bazel-release.pub.gpg | apt-key add -

RUN apt-get update \
  && apt-get install -y bazel \
&& rm -rf /var/lib/apt/lists/*

### --------------- End of python pip anf TF installation ---




# ------------------- opencv dependencies ------------------
RUN mkdir -p /usr/src/app 
WORKDIR /usr/src/app 

# Various Python and C/build deps
RUN apt-get update

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y \ 
    wget \
    build-essential \ 
    cmake \ 
    git \
    unzip \ 
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

RUN apt-get install -y \ 
    python-numpy \ 
    python-pycurl \ 
    libtbb2 \
    libtbb-dev \
    libatlas-base-dev \
    gfortran \
    libvtk6-dev \ 
    zlib1g-dev 
    
#------------ Install Open CV - Warning, this takes absolutely forever
RUN mkdir -p ~/opencv cd ~/opencv && \
    wget https://github.com/Itseez/opencv/archive/3.4.2.zip && \
    unzip 3.4.2.zip && \
    rm 3.4.2.zip && \
    mv opencv-3.4.2 OpenCV && \
    cd OpenCV && \
    mkdir build && \ 
    cd build && \
    cmake \
    -DWITH_IPP=OFF \
    -DWITH_CUDA=OFF \
    -DWITH_QT=OFF \ 
    -DWITH_OPENGL=ON \ 
    -DFORCE_VTK=ON \
    -DWITH_TBB=ON \
    -DWITH_GDAL=ON \
    -DWITH_XINE=ON \
    -DBUILD_EXAMPLES=ON .. && \
    make -j8 && \
    make install && \ 
    ldconfig

COPY . /usr/src/app 
# ------------- end of opencv -------------------



# Jupyter and Tensorboard ports
EXPOSE 8888 6006

WORKDIR "/root"
CMD ["/bin/bash"]


