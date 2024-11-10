import pandas as pd
import time

from deployment.backend.numbers.app import RegexNumberModel  # ЗАМЕНИТЕ НА СВОИ ИМПОРТЫ!
from my_models import TrieEquipmentModel, TrieFailureModel


DATA = 'data/raw/data.csv'  # CHANGE ME!!!
SUBMIT = 'submit.csv'


df = pd.read_csv(DATA, index_col=0)

######################### DATA PREPROCESSING #######################
df['text'] = df['Тема'] + '\n' + df['Описание']
####################################################################


######################### INIT MODELS ##############################
equipment_model = TrieEquipmentModel('trie_equipment.yaml')
failure_model = TrieFailureModel('trie_failure.yaml')
number_model = RegexNumberModel()
####################################################################

start_time = time.time()

df['Тип оборудования'] = df['text'].apply(equipment_model.predict)
df['Точка отказа'] = df['text'].apply(failure_model.predict)
df['Серийный номер'] = df['text'].apply(number_model.predict)

end_time = time.time() - start_time

print(f'Processing time for {df.shape[0]} texts is {end_time} sec')

df.to_csv(SUBMIT, index=False)
