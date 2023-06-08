from transformers import AutoTokenizer, TFAutoModel

model = TFAutoModel.from_pretrained("carlesoctav/multi-qa-en-id-mMiniLMv2-L6-H384")

model.save_pretrained("./model", saved_model=True)