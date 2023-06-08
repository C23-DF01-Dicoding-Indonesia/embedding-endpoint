# Embedding Endpoint

This is an endpoint for embedding text into a vector using the model [carlesoctav/multi-qa-en-id-mMiniLMv2-L6-H384](https://huggingface.co/carlesoctav/multi-qa-en-id-mMiniLMv2-L6-H384).

You can use the ready Docker image from [carlesoctav/my_bert_model](https://hub.docker.com/repository/docker/carlesoctav/my_bert_model). Simply use this command to run the Docker image:

```bash
docker pull carlesoctav/my_bert_model
docker run -d -p 8501:8501 -p 8500:8500 --name carlesoctav/my_bert_model
```

PORT 8501 is for the REST API, and PORT 8500 is for the gRPC API.

## How to use
Take a look at `test_TF_serving_docker.py` for an example of the REST API. Before running the script, make sure the Docker image is running and all the requirements are installed. Then run the script using this command.

## Making the Docker image yourself
If you want to create the Docker image yourself, you can follow these steps:

1. Create a SavedModel. To create a SavedModel, since I saved my model in Hugging Face, I need to convert it to a SavedModel. To do that, I use [save_model_to_TF.py](save_model_to_TF.py) or copy this script:

```python
from transformers import AutoTokenizer, TFAutoModel

model = TFAutoModel.from_pretrained("carlesoctav/multi-qa-en-id-mMiniLMv2-L6-H384")

model.save_pretrained("./model", saved_model=True)
```

2. Create a Docker container with the SavedModel and run it. First, pull the TensorFlow Serving Docker image for CPU (for GPU, replace "serving" with "serving:latest-gpu"):

```bash
docker pull tensorflow/serving
```

3. Next, run the serving image as a daemon named "serving_base":

```bash
docker run -d --name serving_base tensorflow/serving
```

4. Copy the newly created SavedModel into the serving_base container's models folder:

```bash
docker cp my_model/saved_model serving_base:/models/bert
```

5. Commit the container that serves the model by changing "MODEL_NAME" to match the model's name (here, "bert"). The name "bert" corresponds to the name we want to give to our SavedModel:

```bash
docker commit --change "ENV MODEL_NAME bert" serving_base my_bert_model
```

6. Kill the serving_base image that was run as a daemon because we don't need it anymore:

```bash
docker kill serving_base
```

7. Finally, run the image to serve our SavedModel as a daemon. We map the ports 8501 (REST API) and 8500 (gRPC API) in the container to the host, and we name the container "bert":

```bash
docker run -d -p 8501:8501 -p 8500:8500 --name bert my_bert_model
```
