# How to Freeze graph with supervise.ly checkpoint file
## Setup

* Download your model from Supervisely to directory called model
* This will only have checkpoint files
* When you done you should have a model directory in your current working dir that looks like this:
model
model/model_weights
model/model_weights/model.ckpt.meta
model/model_weights/checkpoint
model/model_weights/model.ckpt.index
model/model_weights/model.ckpt.data-00000-of-00001
model/config.json
model/model.config

## Docker
docker run --rm -it \
-v $PWD:/sly_task_data/model \
-w /sly_task_data/model \
supervisely/nn-tf-obj-det:latest \
/bin/bash -l

* The -v just sets the current working director to /sly_task_data/model inside the container
* The -w is the same as cd /sly_task_data/model
* supervisely/nn-tf-obj-det:latest is the docker image we want to use
* /bin/bash will give us a shell

## Docker Setup if you do not have a GPU

* pip install tensorflow==1.5.0
  * Match the version of tensorflow-gpu.  'pip list | grep tensorflow' will give this information

## Simple Script

Now you are ready to freeze your graph
```
import common as com
com.construct_model("./model")
```

Those are the steps that need to be executed, assuming you placed your dowloaded model into the $PWD/model directory(outside docker)
For ease of use I just made this a script:
```
>cat freeze_graph.py
#!/usr/bin/env python
import common as com
com.construct_model("./model")
```
Make sure its executable.

## sample Output

```
root@f57642d6af0e:/sly_task_data/model# pip list | grep tensorflow
tensorflow-gpu         1.5.0
tensorflow-tensorboard 1.5.1
You are using pip version 19.0.3, however version 20.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.


root@f57642d6af0e:/sly_task_data/model# pip install tensorflow==1.5.0
Collecting tensorflow==1.5.0
  Downloading https://files.pythonhosted.org/packages/04/79/a37d0b373757b4d283c674a64127bd8864d69f881c639b1ee5953e2d9301/tensorflow-1.5.0-cp36-cp36m-manylinux1_x86_64.whl (44.4MB)
    100% |████████████████████████████████| 44.4MB 1.3MB/s
Requirement already satisfied: tensorflow-tensorboard<1.6.0,>=1.5.0 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (1.5.1)
Requirement already satisfied: protobuf>=3.4.0 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (3.7.0)
Requirement already satisfied: absl-py>=0.1.6 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (0.7.1)
Requirement already satisfied: numpy>=1.12.1 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (1.14.3)
Requirement already satisfied: six>=1.10.0 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (1.11.0)
Requirement already satisfied: wheel>=0.26 in /usr/local/lib/python3.6/site-packages (from tensorflow==1.5.0) (0.31.1)
Requirement already satisfied: html5lib==0.9999999 in /usr/local/lib/python3.6/site-packages (from tensorflow-tensorboard<1.6.0,>=1.5.0->tensorflow==1.5.0) (0.9999999)
Requirement already satisfied: markdown>=2.6.8 in /usr/local/lib/python3.6/site-packages (from tensorflow-tensorboard<1.6.0,>=1.5.0->tensorflow==1.5.0) (3.1)
Requirement already satisfied: werkzeug>=0.11.10 in /usr/local/lib/python3.6/site-packages (from tensorflow-tensorboard<1.6.0,>=1.5.0->tensorflow==1.5.0) (0.15.2)
Requirement already satisfied: bleach==1.5.0 in /usr/local/lib/python3.6/site-packages (from tensorflow-tensorboard<1.6.0,>=1.5.0->tensorflow==1.5.0) (1.5.0)
Requirement already satisfied: setuptools in /usr/local/lib/python3.6/site-packages (from protobuf>=3.4.0->tensorflow==1.5.0) (39.2.0)
Installing collected packages: tensorflow
Successfully installed tensorflow-1.5.0
You are using pip version 19.0.3, however version 20.0.2 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.


root@f57642d6af0e:/sly_task_data/model# ./freeze_graph.py
{"message": "Freezing training checkpoint!", "timestamp": "2020-02-13T14:34:19.041Z", "level": "info"}
WARN:tensorflow:From /workdir/src/models/research/object_detection/exporter.py:351: get_or_create_global_step (from tensorflow.contrib.framework.python.ops.variables) is deprecated and will be removed in a future version.
Instructions for updating:
Please switch to tf.train.get_or_create_global_step
2020-02-13 14:34:23.911192: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX AVX2 FMA
Converted 344 variables to const ops.
{"message": "Restored model weights from training.", "timestamp": "2020-02-13T14:34:26.600Z", "level": "info"}


root@f57642d6af0e:/sly_task_data/model# ls model/
config.json  model.config  model.pb  model_weights


root@f57642d6af0e:/sly_task_data/model# ls model/model.pb
model/model.pb
```
