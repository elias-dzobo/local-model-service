""" Test Framework """

#internal
from src.pipeline.main import fetch_model, fetch_model_from_path

def main():
    fetch_model("google/functiongemma-270m-it")
    #fetch_model_from_path("/Users/eliasdzobo/Desktop/local-model-service/model/whisper-tiny")



if __name__ == '__main__':
    main()