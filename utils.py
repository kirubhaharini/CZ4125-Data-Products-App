"""
Other utility objects
"""
import numpy as np
import secrets

class IDMAP(object):
    """
    converts ids to indexes. vice versa.
    args:
        - entity_ids; list of real ids of the entities e.g item ids or user ids
    """
    def __init__(self, entity_ids):
        self.entity_ids = np.array(entity_ids)
        self.id_to_index_map = {v:k for k,v in enumerate(entity_ids)}
    def get_ids(self, indexes):
        return self.entity_ids[indexes]
    def get_indexes(self, ids):
        return [self.id_to_index_map[i] for i in ids]
    
    