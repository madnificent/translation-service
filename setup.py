from transformers import MarianMTModel, MarianTokenizer

tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-nl-en")
model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-nl-en", torch_dtype="auto")

# save to /data
tokenizer.save_pretrained("/data/tokenizer")
model.save_pretrained("/data/model")

print("Saved models in the image to /data/")
