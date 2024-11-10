from typing import List

import pandas as pd
import time

from deployment.backend.numbers.app import RegexNumberModel  # ЗАМЕНИТЕ НА СВОИ ИМПОРТЫ!
from deployment.backend.equipment.model import EquipmentModel
from deployment.backend.failure.model import FailureModel

# from deployment.backend.equipment.app import TextClassifier


DATA = './submit_sample.csv'  # CHANGE ME!!!
SUBMIT = 'submit.csv'


df = pd.read_csv(DATA, index_col=0)

######################### DATA PREPROCESSING #######################
df['text'] = df['Тема'] + '\n' + df['Описание']
df['text_'] = df['Тема'] + " [SEP] " + df['Описание']
df['text__'] = df['Тема'] + "[SEP]" + df['Описание']
####################################################################


######################### INIT MODELS ##############################
equipment_model = EquipmentModel('./EQUIPMENT_rubert_tiny_v1.pt')
failure_model = FailureModel('./FAILED_rubert_tiny_v1.pt.pt')
# failure_model_v2 = TextClassifier(model_path="failure-model", tokenizer_path="failure-model")
number_model = RegexNumberModel()
####################################################################

start_time = time.time()


def model_predict(model, data: pd.core.series.Series) -> List[str]:
    sentences = model.predict(data.to_list())
    return [sentence.tag for sentence in sentences]


# def failure_model_v2_predict(texts: List[str]) -> List[str]:
#    predictions = failure_model_v2.classifier(texts)
#    labels = [pred['label'] for pred in predictions]
#    return labels


# df['Тип оборудования'] = df['text_'].apply(equipment_model.predict)
df['Тип оборудования'] = model_predict(equipment_model, df['text_'])
df['Точка отказа'] = model_predict(failure_model, df['text_'])

df['Точка отказа'] = df['text'].apply(failure_model.predict)
# df['Точка отказа'] = df['text__'].apply(failure_model_v2.predict)
df['Серийный номер'] = df['text'].apply(number_model.predict)

end_time = time.time() - start_time

print(f'Processing time for {df.shape[0]} texts is {end_time} sec')

df.to_csv(SUBMIT, index=False)
