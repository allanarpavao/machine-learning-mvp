from sklearn.metrics import accuracy_score, f1_score, recall_score
import pickle
import pickle
import pandas as pd
from pathlib import Path


class Preprocessador:
    def __init__(self, atributos_do_modelo):
        """ Extrai a ordem correta das colunas.
        """
        self.colunas_ordenadas = atributos_do_modelo.feature_names_in_


    def preparar_dados_body(self, body):
        """ Recebe os dados do front e transforma em dataframe.
        """
        dados_forms_em_dict = body.model_dump()
        dados_em_dataframe = pd.DataFrame([dados_forms_em_dict], columns=self.colunas_ordenadas)

        return dados_em_dataframe


class Pipeline:
    
    def __init__(self):
        """Inicializa o pipeline
        """
        self.pipeline = None
    
    def carrega_pipeline(self):
        """Carrega o pipeline construído
        """
        caminho_pasta_api = Path(__file__).resolve().parents[1]
        caminho_pipeline_pkl = caminho_pasta_api / 'MachineLearning' / 'models' / 'students_pipeline.pkl'

        with open(caminho_pipeline_pkl, 'rb') as file:
            self.pipeline = pickle.load(file)
        
        return self.pipeline

    def preditor(self, X_input):
        """Realiza a predição da situaçao academica de um estudante com base no modelo treinado
        """
        if self.pipeline is None:
            raise RuntimeError('O pipeline não foi carregado antes da predição.')
        
        results = self.pipeline.predict(X_input)
        return results

    def preditor_proba(self, X_input):
        """Retorna as probabilidades de cada classe.
        """
        if self.pipeline is None:
            raise RuntimeError('O pipeline não foi carregado antes da predição.')
        
        return self.pipeline.predict_proba(X_input)


class Avaliador:
    def __init__(self):
        pass

    def avaliar_acuracia(self, modelo, X, y_true):
        y_pred = modelo.preditor(X)
        return accuracy_score(y_true, y_pred)
        
    def avaliar_recall(self, modelo, X, y_true):
        y_pred = modelo.preditor(X)
        return recall_score(y_true, y_pred, average='weighted')
        
    def avaliar_f1(self, modelo, X, y_true):
        y_pred = modelo.preditor(X)
        return f1_score(y_true, y_pred, average='weighted')