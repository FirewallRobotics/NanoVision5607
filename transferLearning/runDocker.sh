#!/bin/bash
docker run --rm -it \
	-v $PWD:/sly_task_data/model' \
	supervisely/nn-tf-obj-det:latest \
	"$@"
