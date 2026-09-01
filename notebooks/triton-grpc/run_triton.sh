#!/bin/bash
# Run the example model repository.

docker run --rm -p8000:8000 -p8001:8001 -p8002:8002 -v$(pwd)/model_repository:/models nvcr.io/nvidia/tritonserver:23.10-py3 tritonserver --model-repository=/models
