import pickle
import pandas as pd
import pickle
import numpy as np
from pathlib import Path


class Preprocessador:
# FIXME:
    def preparar_form(self, form):
        """ Prepara os dados recebidos do front para serem usados no modelo. """
        X_input = np.array([form.preg, 
                            form.plas, 
                            form.pres, 
                            form.skin, 
                            form.test, 
                            form.mass, 
                            form.pedi, 
                            form.age
                        ])
        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)
        return X_input
    
    def preparar_array_lista(self, dados_lista):
        """" Transforma dados em lista em array Numpy
        """
        X_input = np.array(dados_lista)
        X_input = X_input.reshape(1, -1)

        return X_input

    # def scaler(self, X_train):
    #     """ Normaliza os dados. """
    #     scaler = pickle.load(open('./MachineLearning/models/minmax_scaler_students.pkl', 'rb'))
    #     reescaled_X_train = scaler.transform(X_train)

    #     return reescaled_X_train


# class Modelo:
    
#     def __init__(self):
#         """Inicializa o modelo
#         """
#         self.model = None
    
#     def carrega_modelo(self, path):
#         """Carrega o modelo construído
#         """

#         with open(path, 'rb') as file:
#             self.model = pickle.load(file)
       
#         return self.model
    

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

# TODO:
    def preditor_proba(self, X_input):
        """ Retorna as probabilidades de cada classe. """
        if self.pipeline is None:
            raise RuntimeError('O pipeline não foi carregado antes da predição.')
        
        return self.pipeline.predict_proba(X_input)


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

    # Inicializar pipeline:
    best_pipeline = Pipeline()
    caminho_pipeline_pkl = '../MachineLearning/models/students_pipeline.pkl'
    best_pipeline.carrega_pipeline()

    # Predicao
    nova_avaliacao_estudante = best_pipeline.preditor(dados_in_array)
    probabilidades = best_pipeline.preditor_proba(dados_in_array)

    print(f"\nA categoria prevista para o aluno é: {nova_avaliacao_estudante[0]}")
    print(f"As probabilidades para cada classe são: {probabilidades[0]}")
