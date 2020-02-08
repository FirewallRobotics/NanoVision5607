#!/bin/bash
docker run --rm -it \
	--runtime=nvidia \
	-p 5000:5000 \
	-v $PWD'/PowerCell:/sly_task_data/model' \
	supervisely/nn-tf-obj-det:latest \
	"$@"
	python /workdir/src/rest_inference.pysupervisely/nn-tf-obj-det:latest
