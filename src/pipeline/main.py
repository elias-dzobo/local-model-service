import os
from transformers import pipeline, AutoModel, AutoConfig, AutoTokenizer

def fetch_model(name: str, model_directory = "/Users/eliasdzobo/Desktop/local-model-service/model"):
    model = AutoModel.from_pretrained(name)
    config = AutoConfig.from_pretrained(name)
    tokenizer = AutoTokenizer.from_pretrained(name)

    dir_name = name.split('/')[-1]
    model_directory = os.path.join(model_directory, dir_name)

    if not os.path.exists(model_directory):
        os.mkdir(model_directory)

    model.save_pretrained(model_directory)
    tokenizer.save_pretrained(model_directory)
    config.save_pretrained(model_directory)


    print(config)

def fetch_model_from_path(path: str):
    model = AutoModel.from_pretrained(path)
    config = AutoConfig.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)

    print(config)