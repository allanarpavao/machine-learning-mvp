from sklearn.metrics import accuracy_score, f1_score, recall_score
import pickle
import pickle
import numpy as np
from pathlib import Path


class Preprocessador:
    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo.
        """
        
        valores_em_lista = list(form.model_dump().values())
        X_input = np.array(valores_em_lista)

        X_input = X_input.reshape(1, -1)
        return X_input

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



### Teste:
if __name__ == '__main__':
    dados_in = [[
        2, 39, 1, 8014, 0, 1, 100.0, 1, 37, 38, 9, 9, 141.5, 
        0, 0, 0, 1, 0, 0, 45, 0, 0, 6, 9, 5, 12.334, 0, 0, 
        6, 6, 6, 13.0, 0
    ]]

    print("teste local:")
    
    # Pre processamento de dados:
    preprocessador = Preprocessador()
    dados_in_array = preprocessador.preparar_array_lista(dados_in)
    breakpoint()

    # Inicializar pipeline:
    best_pipeline = Pipeline()
    best_pipeline.carrega_pipeline()

    # Predicao
    nova_avaliacao_estudante = best_pipeline.preditor(dados_in_array)
    probabilidades = best_pipeline.preditor_proba(dados_in_array)

    print(f"\nA categoria prevista para o aluno é: {nova_avaliacao_estudante[0]}")
    print(f"As probabilidades para cada classe são: {probabilidades[0]}")
