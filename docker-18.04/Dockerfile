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

###---------------- End of Nvidia Cuda CUDNN -------------------



RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python3-dev python3-pip \
    libfreetype6-dev libpng-dev libhdf5-dev
    
RUN apt-get update && apt-get install -y wget ca-certificates \
    git curl vim python2.7-dev python-pip 

RUN pip3 install --upgrade pip
RUN pip3 install tensorflow
RUN pip3 install numpy pandas sklearn matplotlib jupyter pyyaml h5py seaborn
RUN pip3 install keras --no-deps
RUN pip3 install flask
RUN pip3 install mysql-connector
RUN pip3 install xgboost
RUN pip3 install statsmodels
RUN pip3 install gunicorn
RUN python3 -m pip install ipykernel
RUN python3 -m ipykernel install --user

RUN pip2 install --upgrade pip
RUN pip2 install tensorflow
RUN pip2 install numpy pandas sklearn matplotlib jupyter pyyaml h5py seaborn
RUN pip2 install keras --no-deps
RUN pip2 install flask
RUN pip2 install mysql-connector
RUN pip2 install xgboost
RUN pip2 install statsmodels
RUN pip2 install gunicorn

## ---- Bazel
RUN apt-get update && apt-get install -y openjdk-8-jdk
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | tee /etc/apt/sources.list.d/bazel.list \
  && curl https://bazel.build/bazel-release.pub.gpg | apt-key add -

RUN apt-get update \
  && apt-get install -y bazel \
&& rm -rf /var/lib/apt/lists/*
### --------------- End of python pip anf TF installation ---



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
WORKDIR /
RUN pwd
RUN wget https://github.com/Itseez/opencv/archive/3.4.2.zip -O opencv.zip \
	&& unzip /opencv.zip \
	&& wget https://github.com/Itseez/opencv_contrib/archive/3.4.2.zip -O opencv_contrib.zip \
	&& unzip /opencv_contrib \
	&& mkdir opencv-3.4.2/cmake_binary \
	&& cd opencv-3.4.2/cmake_binary \
	&& cmake -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib-3.4.2/modules \
	  -DBUILD_TIFF=ON \
	  -DBUILD_opencv_java=OFF \
	  -DWITH_CUDA=OFF \
	  -DENABLE_AVX=ON \
	  -DWITH_OPENGL=ON \
	  -DWITH_OPENCL=ON \
	  -DWITH_IPP=ON \
	  -DWITH_TBB=ON \
	  -DWITH_EIGEN=ON \
	  -DWITH_V4L=ON \
	  -DBUILD_TESTS=OFF \
	  -DBUILD_PERF_TESTS=OFF \
	  -DCMAKE_BUILD_TYPE=RELEASE \
	  -DBUILD_opencv_python3=ON \
	  -DCMAKE_INSTALL_PREFIX=$(python3.6 -c "import sys; print(sys.prefix)") \
	  -DPYTHON_EXECUTABLE=$(which python3.6) \
	  -DPYTHON_INCLUDE_DIR=$(python3.6 -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
	  -DPYTHON_PACKAGES_PATH=$(python3.6 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") .. \
	&& make install \
	&& rm /opencv.zip \
	&& rm /opencv_contrib.zip \
	&& rm -r /opencv-3.4.2 \
	&& rm -r /opencv_contrib-3.4.2

COPY . /usr/src/app 
# ------------- end of opencv -------------------



# Jupyter and Tensorboard ports
EXPOSE 8888 6006

WORKDIR "/root"
CMD ["/bin/bash"]


