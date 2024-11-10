from flair.data import Corpus, Sentence
from flair.datasets import TREC_6, CSVClassificationCorpus
from flair.embeddings import TransformerDocumentEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer

import torch
import argparse
import json
import csv
import mlflow
import re
import time

import pandas as pd

def get_model_size(document_embeddings):
    param_size = 0
    for param in document_embeddings.parameters():
        param_size += param.nelement() * param.element_size()
    buffer_size = 0
    for buffer in document_embeddings.buffers():
        buffer_size += buffer.nelement() * buffer.element_size()
    
    size_all_mb = (param_size + buffer_size) / 1024**2
    return '{:.3f}MB'.format(size_all_mb)

def remove_symbols(text):
    return re.sub(r'[^A-Za-z0-9\s]', '', text.strip())


mlflow.set_tracking_uri(uri="http://127.0.0.1:8082")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the text classification training script with specified parameters.')
    parser.add_argument('--experiment', type=str, default='./data/', help='Exp name')
    parser.add_argument('--data_folder', type=str, default='./data/', help='Path to the data folder')
    parser.add_argument('--model_name', type=str, default='deepvk/USER-base', help='Model name for the transformer embeddings')
    parser.add_argument('--learning_rate', type=float, default=5.0e-5, help='Learning rate for training')
    parser.add_argument('--mini_batch_size', type=int, default=32, help='Mini batch size for training')
    parser.add_argument('--max_epochs', type=int, default=5, help='Maximum number of epochs for training')
    
    args = parser.parse_args()
    
    # Use arguments
    mlflow.set_experiment(args.experiment)
    data_folder = args.data_folder
    model_name = args.model_name
    learning_rate = args.learning_rate
    mini_batch_size = args.mini_batch_size
    max_epochs = args.max_epochs
    
    
    with mlflow.start_run():
    
        
        mlflow.log_artifacts(data_folder, artifact_path="data")
        
        column_name_map = {0: "text", 1: "label"}
        corpus: Corpus = CSVClassificationCorpus(data_folder,
                                                 column_name_map,
                                                 skip_header=False,
                                                 delimiter='\t',    # tab-separated files
                                                 label_type='label')
    
        mlflow.log_param("train_data_length", len(corpus.train))
        mlflow.log_param("test_data_length", len(corpus.test))
    
        label_dict = corpus.make_label_dictionary(label_type='label')
        document_embeddings = TransformerDocumentEmbeddings(model_name, fine_tune=True)
        classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, label_type='label')
    
        max_length: int = document_embeddings.tokenizer.model_max_length
        model_size_mb: str = get_model_size(document_embeddings)
        model_hidden_size: int = document_embeddings.model.config.hidden_size
        mlflow.log_param("model_name", model_name)
        mlflow.log_param("max_length", max_length)
        mlflow.log_param("model_size_mb", model_size_mb)
        mlflow.log_param("model_hidden_size", model_hidden_size)
    
    
        mlflow.log_param("learning_rate", learning_rate)
        mlflow.log_param("mini_batch_size", mini_batch_size)
        mlflow.log_param("max_epochs", max_epochs)
        mlflow.log_param("train_with_dev", "true")
        trainer = ModelTrainer(classifier, corpus)
        model_path = remove_symbols(data_folder) + "/" + model_name.replace("/", "_").replace("-", "_")

        model_folder = "modelsv3"
        
        trainer.fine_tune(f'{model_folder}/{model_path}',
                          learning_rate=learning_rate,
                          mini_batch_size=mini_batch_size,
                          max_epochs=max_epochs,
                          monitor_test=True, train_with_dev=True)
    
        del classifier, trainer
        
        model = TextClassifier.load(f'{model_folder}/{model_path}/final-model.pt')
        
        start_time = time.time()
        result = model.evaluate(corpus.test, gold_label_type='label', mini_batch_size=mini_batch_size)
        end_time = time.time()


        execution_time_seconds = end_time - start_time
        execution_time_minutes = execution_time_seconds / 60
        mlflow.log_param("evaluate_time", execution_time_minutes)
        
        for category, metrics in result.classification_report.items():
            if isinstance(metrics, dict):
                for metric_name, metric_value in metrics.items():
                    mlflow.log_metric(f"{category}_{metric_name}", metric_value)
            else:
                mlflow.log_metric(category, metrics)
        
    
        with open("metrics.json", "w") as f:
            json.dump(result.classification_report, f)
        mlflow.log_artifact("metrics.json", "metrics")
        
        with open("results_table.txt", "w") as file:
            file.write(result.detailed_results)
        mlflow.log_artifact("results_table.txt", "classification_report")
    
        mlflow.log_artifacts(f'{model_folder}/{model_path}', "model")
    
        del model
        torch.cuda.empty_cache()