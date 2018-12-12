

## All-in-one Docker image for Deep Learning
Here are Dockerfiles to get you up and running with a fully functional deep learning machine. It contains all the popular deep learning frameworks with CPU and GPU support (CUDA and cuDNN included). The CPU version should work on Linux, Windows and OS X. The GPU version will, however, only work on Linux machines. See [OS support](#what-operating-systems-are-supported) for details

If you are not familiar with Docker, but would still like an all-in-one solution, start here: [What is Docker?](#what-is-docker). If you know what Docker is, but are wondering why we need one for deep learning, [see this](#why-do-i-need-a-docker)

## Specs
### For Ubuntu 18.04 Docker
This is what you get out of the box when you create a container with the provided image/Dockerfile:
* Ubuntu 18.04
* [CUDA 9.2](https://developer.nvidia.com/cuda-toolkit)
* [cuDNN 7](https://developer.nvidia.com/cudnn)
* [Tensorflow-gpu](https://www.tensorflow.org/)
* [Keras](http://keras.io/)
* [iPython/Jupyter Notebook](http://jupyter.org/) 
* [Numpy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), [Pandas](http://pandas.pydata.org/), [Scikit Learn](http://scikit-learn.org/), 
[Matplotlib](http://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), [Xgboost](https://xgboost.readthedocs.io/en/latest/), [Statmodels](https://pypi.org/project/statsmodels/),
Jupyter  (python2 and 3)
* [OpenCV 3.4](http://opencv.org/) + Contrib
* [Flask](http://flask.pocoo.org/)
* Mysql-connector


### For Ubuntu 16.04 Docker
This is what you get out of the box when you create a container with the provided image/Dockerfile:
* Ubuntu 16.04
* [CUDA 8](https://developer.nvidia.com/cuda-toolkit)
* [cuDNN 5](https://developer.nvidia.com/cudnn)
* [Tensorflow-gpu 1.4.1](https://www.tensorflow.org/)
* [Keras](http://keras.io/)
* [iPython/Jupyter Notebook](http://jupyter.org/) 
* [Numpy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), [Pandas](http://pandas.pydata.org/), [Scikit Learn](http://scikit-learn.org/), 
[Matplotlib](http://matplotlib.org/), [Seaborn](https://seaborn.pydata.org/), [Xgboost](https://xgboost.readthedocs.io/en/latest/), [Statmodels](https://pypi.org/project/statsmodels/),
Jupyter (for python2 and 3)
* [OpenCV 3.4](http://opencv.org/) + Contrib
* [Flask](http://flask.pocoo.org/)
* Mysql-connector


### Gogle Cloud K80 GPU Note
* **You should install nvidia driver**

```
curl -O https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.0.176-1_amd64.deb  
sudo dpkg -i cuda-repo-ubuntu1604_9.0.176-1_amd64.deb  
sudo apt-get update  
```

* **Sincronize the driver**

```
sudo nvidia-smi -pm 1  
```

* **Check the Driver**

```
nvidia-smi
```

* **If these steps don't work, try to install automatically by this:**
```
sudo apt install ubuntu-drivers-common
```
* **Or this:**
```
sudo ubuntu-drivers autoinstall
```

* **The last, BUILD YOUR DOCKER FILE**

### CUDA and CUDNN Note For Tensorflow
> Tensorflow 1.4.x: CUDNN 6.0 and CUDA 8.0
> Tensorflow 1.7.x: CUDNN 7.0 and CUDA 9.0

