import json
from azureml.core.model import Model

def init():
    global model
    model_path = Model.get_model_path("base")
    print("Model Path is  ", model_path)
    model = joblib.load(model_path)


def run(data):
    test = json.loads(data)
    print(f"received data {test}")
    return model.predict(test)
    # return f"test is {test}"