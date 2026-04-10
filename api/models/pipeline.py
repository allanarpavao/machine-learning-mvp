import pickle

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