#!/bin/bash
docker run --rm -it \
	-v $PWD:/sly_task_data/model \
	-w /sly_task_data/model \
	team5607/sly/nn-tf-obj-det:latest \
	/bin/bash -l 
#	sh -c "./freeze_graphy.py"
