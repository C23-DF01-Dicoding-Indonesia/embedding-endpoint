from transformers import AutoTokenizer, TFAutoModel
import requests
import json
import numpy as np

sentence = "Hallo Dunia"

# Load the corresponding tokenizer of our SavedModel
tokenizer = AutoTokenizer.from_pretrained("carlesoctav/multi-qa-en-id-mMiniLMv2-L6-H384")

# Load the model config of our SavedModel

# Tokenize the sentence
batch = tokenizer(sentence)

# Convert the batch into a proper dict
batch = dict(batch)

# Put the example into a list of size 1, that corresponds to the batch size
batch = [batch]

print(batch)

# The REST API needs a JSON that contains the key instances to declare the examples to process
input_data = {"instances": batch}

# Query the REST API, the path corresponds to http://host:port/model_version/models_root_folder/model_name:method
r = requests.post("http://localhost:8501/v1/models/bert:predict", data=json.dumps(input_data))

# Parse the JSON result. The results are contained in a list with a root key called "predictions"
# and as there is only one example, takes the first element of the list
result = json.loads(r.text)["predictions"][0]["last_hidden_state"][0]

print(result)

