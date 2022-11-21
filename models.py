"""
Recommendation Models
"""

# from implicit.als import AlternatingLeastSquares

# from implicit.gpu.als import AlternatingLeastSquares
# from implicit.gpu.bpr import BayesianPersonalizedRanking
# from implicit.gpu.matrix_factorization_base import MatrixFactorizationBase

from implicit.cpu.als import AlternatingLeastSquares
from implicit.cpu.bpr import BayesianPersonalizedRanking
from implicit.cpu.lmf import LogisticMatrixFactorization
import pickle
import os


class BaseRecommender(object):
    def fit(self):
        raise NotImplementedError
    def recommend(self):
        raise NotImplementedError
        
class ALSRecommender(BaseRecommender):
    def __init__(self, model_name, config_dict, train_csr, user_map, item_map):
        
        self.config_dict = config_dict
        if model_name == "AlternatingLeastSquares":
            self.model = AlternatingLeastSquares(**self.config_dict)
        elif model_name == "BayesianPersonalizedRanking":
            self.model = BayesianPersonalizedRanking(**self.config_dict)
        elif model_name == "LogisticMatrixFactorization":
            self.model = LogisticMatrixFactorization(**self.config_dict)
        else:
            raise Exception("Model not found")
        
        self.train_csr = train_csr
        self.user_map = user_map
        self.item_map = item_map
        super(ALSRecommender, self).__init__()
        
    def fit(self, show_progress = False):
        self.model.fit(self.train_csr, show_progress = show_progress)
    def recommend(self, user_id, num_rec = 20, filtered_item_ids = []):
        user_index = self.user_map.get_indexes([user_id])[0]
        filtered_item_indexes = self.item_map.get_indexes(filtered_item_ids)
        recommended_items_index, scores = self.model.recommend(user_index, self.train_csr[user_index], num_rec, filter_items = filtered_item_indexes)
        recommended_item_ids = self.item_map.get_ids(recommended_items_index)
        return recommended_item_ids
    
        
    def load(self, directory = r"C:\Users\tanch\Documents\NTU\NTU Year 4\Semester 1\CZ4125 - Developing Data Products\Assignments\Team Assignment - book recommendation\code\models"):
        self.model = self.model.load(os.path.join(directory,"final_recommender.npz"))
        with open(os.path.join(directory,"item_map.pkl"),"rb") as f:
            self.item_map = pickle.load( f)
        with open(os.path.join(directory,"user_map.pkl"),"rb") as f:
            self.user_map = pickle.load( f)
        with open(os.path.join(directory,"train_csr.pkl"),"rb") as f:
            self.train_csr = pickle.load( f)
    def save(self, path):
        self.model.save(path)
        
        
class PopRecommender(BaseRecommender):
    def fit(self, train):
        self.train = train
        self.memory = train.ISBN.value_counts().keys().tolist()
    def recommend(self, user_id, num_rec = 20, filtered_item_ids = []):
        remove_item_ids = self._get_user_liked_item_ids(user_id)
        remove_item_ids += filtered_item_ids
        candidates = self.memory
        for item_id in remove_item_ids:
            if item_id in candidates: 
                candidates.remove(item_id)
        return candidates[:num_rec]
        
    def _get_user_liked_item_ids(self, user_id):
        return self.train[self.train['User-ID'] == user_id].ISBN.tolist()
    
#     def save(self, path):
#         with open(path, "wb") as f:
#             pickle.dump(self.memory, f)
#     def load(self, path):
#         with open(path, "rb") as f:
#             self.memory = pickle.load(f)