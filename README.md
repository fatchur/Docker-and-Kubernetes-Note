

## All-in-one Docker image for Deep Learning
Here are Dockerfiles to get you up and running with a fully functional deep learning machine. It contains all the popular deep learning frameworks with CPU and GPU support (CUDA and cuDNN included). The CPU version should work on Linux, Windows and OS X. The GPU version will, however, only work on Linux machines. See [OS support](#what-operating-systems-are-supported) for details

If you are not familiar with Docker, but would still like an all-in-one solution, start here: [What is Docker?](#what-is-docker). If you know what Docker is, but are wondering why we need one for deep learning, [see this](#why-do-i-need-a-docker)

## Update: I've built a quick tool, based on dl-docker, to run your DL project on the cloud with zero setup. You can start running your Tensorflow project on AWS in <30seconds using Floyd. See [www.floydhub.com](https://www.floydhub.com). It's free to try out. 
### Happy to take feature requests/feedback and answer questions - mail me sai@floydhub.com.

## Specs
This is what you get out of the box when you create a container with the provided image/Dockerfile:
* Ubuntu 14.04
* [CUDA 9.2](https://developer.nvidia.com/cuda-toolkit)
* [cuDNN 7](https://developer.nvidia.com/cudnn)
* [Tensorflow](https://www.tensorflow.org/)
* [Keras](http://keras.io/)
* [iPython/Jupyter Notebook](http://jupyter.org/) (including iTorch kernel)
* [Numpy](http://www.numpy.org/), [SciPy](https://www.scipy.org/), [Pandas](http://pandas.pydata.org/), [Scikit Learn](http://scikit-learn.org/), [Matplotlib](http://matplotlib.org/)
* [OpenCV](http://opencv.org/)
