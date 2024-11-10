from typing import List

import pandas as pd
import time

from deployment.backend.numbers.app import RegexNumberModel  # ЗАМЕНИТЕ НА СВОИ ИМПОРТЫ!
from deployment.backend.equipment.model import EquipmentModel


DATA = 'data/raw/data.csv'  # CHANGE ME!!!
SUBMIT = 'submit.csv'


df = pd.read_csv(DATA, index_col=0)

######################### DATA PREPROCESSING #######################
df['text'] = df['Тема'] + '\n' + df['Описание']
df['text_'] = df['Тема'] + " [SEP] " + df['Описание']
####################################################################


######################### INIT MODELS ##############################
equipment_model = EquipmentModel('./final-model.pt')
failure_model = TrieFailureModel('trie_failure.yaml')
number_model = RegexNumberModel()
####################################################################

start_time = time.time()


def equipment_model_predict(data: pd.core.series.Series) -> List[str]:
    sentences = equipment_model.predict(data.to_list())
    return [sentence.tag for sentence in sentences]


# df['Тип оборудования'] = df['text_'].apply(equipment_model.predict)
df['Тип оборудования'] = equipment_model_predict(df['text_'])
df['Точка отказа'] = df['text'].apply(failure_model.predict)
df['Серийный номер'] = df['text'].apply(number_model.predict)

end_time = time.time() - start_time

print(f'Processing time for {df.shape[0]} texts is {end_time} sec')

df.to_csv(SUBMIT, index=False)