from models.machine_learning import *
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

# To run: python3 -m pytest -v test_modelos.py

preprocessador = Preprocessador()
pipeline = Pipeline()
avaliador = Avaliador()

url_dados = "./MachineLearning/data/dataset.csv"

dataframe = pd.read_csv(url_dados, delimiter=';')
colunas_para_remover = ["Unemployment rate", "Inflation rate", "GDP"]
students_dataframe = dataframe.drop(columns=colunas_para_remover)

X = students_dataframe.iloc[:, 0:-1].values  
y_true = students_dataframe.iloc[:, -1].values 

def test_modelo_estudantes():
    pipeline.carrega_pipeline()

    acuracia = avaliador.avaliar_acuracia(pipeline, X, y_true)
    assert acuracia >= 0.75

    recall = avaliador.avaliar_recall(pipeline, X, y_true)
    assert recall >= 0.75

    f1 = avaliador.avaliar_f1(pipeline, X, y_true)
    assert f1 >= 0.70
from sklearn.dummy import DummyClassifier


def test_modelo_inadequado():
    """
    Testa um modelo dummy para garantir que só modelos com valores
    compatíveis funcionam
    """
    modelo_dummy = DummyClassifier(strategy="most_frequent")
    modelo_dummy.fit(X, y_true)
    
    y_pred = modelo_dummy.predict(X)
    
    acuracia = accuracy_score(y_true, y_pred)

    assert acuracia >= 0.75
