import os

from transformers import pipeline

os.environ["CUDA_VISIBLE_DEVICES"] =  ""

from typing import List

import pandas as pd
import time

from deployment.backend.numbers.app import RegexNumberModel  # ЗАМЕНИТЕ НА СВОИ ИМПОРТЫ!
from deployment.backend.equipment.nn import EquipmentModel
from deployment.backend.failure.nn import FailureModel

class TextClassifier:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.classifier = pipeline("text-classification", model=model_path, tokenizer=tokenizer_path)

    def predict(self, texts: List[str]) -> List[str]:
        return self.classifier(texts)


import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

DATA = './test_data.csv'  # CHANGE ME!!!
SUBMIT = 'submit_2_1.csv'

pairs = [["EQ_deepvk_USER_base_v1.pt", None],
    ["EQ_deepvk_USER_bge_m3_v1.pt", "EQ_deepvk_USER_bge_m3_v1.pt"],
         ["EQ_deepvk_USER_bge_m3_v1_DEV.pt", "FA_deepvk_USER_bge_m3_v1_DEV.pt"],
         ["EQ_deepvk_USER_base_v1.pt", "FA_deepvk_USER_base_v1.pt"],
         ["EQ_deepvk_USER_base_v1_DEV.pt", "FA_deepvk_USER_base_v1_DEV.pt"]]


eq, fl = pairs[0]


df = pd.read_csv(DATA, sep=',').fillna("")

######################### DATA PREPROCESSING #######################
df['text'] = df['Тема'] + '\n' + df['Описание']
df['text_'] = df['Тема'] + " [SEP] " + df['Описание']
df['text__'] = df['Тема'] + "[SEP]" + df['Описание']
####################################################################


######################### INIT MODELS ##############################
equipment_model = EquipmentModel(f'./{eq}')
# failure_model = FailureModel(f'./{fl}')
failure_model_v2 = TextClassifier(model_path="./tiny2-82", tokenizer_path="./tiny2-82")
number_model = RegexNumberModel()
####################################################################

start_time = time.time()


def model_predict(model, data: pd.core.series.Series) -> List[str]:
    sentences = model.predict(data.to_list(), 1)
    return [sentence.tag for sentence in sentences]


def failure_model_v2_predict(texts: List[str]) -> List[str]:
    predictions = failure_model_v2.classifier(texts)
    labels = [pred['label'] for pred in predictions]
    return labels


# df['Тип оборудования'] = df['text_'].apply(equipment_model.predict)
df['Тип оборудования'] = model_predict(equipment_model, df['text_'])
# df['Точка отказа'] = model_predict(failure_model, df['text_'])

# df['Точка отказа'] = df['text'].apply(failure_model.predict)

df['Точка отказа'] = failure_model_v2_predict(df['text__'].to_list())
# df['Точка отказа'] = df['text__'].apply(failure_model_v2.predict)
df['Серийный номер'] = df['text'].apply(lambda x: number_model.predict([x])[0])

end_time = time.time() - start_time

print(f'Processing time for {df.shape[0]} texts is {end_time} sec')

df.drop(columns=['Тема', 'Описание', 'text', 'text_', 'text__']).to_csv(SUBMIT, index=False)
