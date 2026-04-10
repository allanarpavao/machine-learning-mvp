import pickle

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