import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class Preprocessador:    
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
    
    def scaler(self, X_train):
        """ Normaliza os dados. """
        # normalização/padronização
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_diabetes.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train


class Modelo:
    
    def __init__(self):
        """Inicializa o modelo
        """
        self.model = None
    
    def carrega_modelo(self, path):
        """Carrega o modelo construído
        """

        with open(path, 'rb') as file:
            self.model = pickle.load(file)
       
        return self.model
    
    def preditor(self, X_input):
        """Realiza a predição da situaçao academica de um estudante com base no modelo treinado
        """
        if self.model is None:
            raise Exception('Modelo não foi carregado. Use carrega_modelo() primeiro.')
        
        results = self.model.predict(X_input)
        return results


class Pipeline:
    
    def __init__(self):
        """Inicializa o pipeline
        """
        self.pipeline = None
    
    def carrega_pipeline(self, path):
        """Carrega o pipeline construído
        """
        
        with open(path, 'rb') as file:
             self.pipeline = pickle.load(file)
             
        return self.pipeline



### Teste:
if __name__ == '__main__':
    dados_in = [[
        2, 39, 1, 8014, 0, 1, 100.0, 1, 37, 38, 9, 9, 141.5, 
        0, 0, 0, 1, 0, 0, 45, 0, 0, 6, 9, 5, 12.334, 0, 0, 
        6, 6, 6, 13.0, 0
    ]]

    dados_in_array = np.array(dados_in)
    nova_predicao = best_pipeline.predict(dados_in_array)
    probabilidades = best_pipeline.predict_proba(dados_in_array)


    # print(f"A categoria prevista para o aluno é: {nova_predicao[0]}")
    # print(f"As probabilidades para cada classe são: {probabilidades[0]}")