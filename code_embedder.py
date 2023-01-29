from typing import Any, Dict, List, Tuple
import os
import nmslib
from openai.embeddings_utils import get_embedding
from repository import BASE_PATH
from format_utils import cprint

BASE_PATH = os.path.expanduser("~/data/indexes/")

class CodeEmbeddingIndexer:
    def __init__(self, code_root: str, code_funcs: List[Dict[str, Any]]) -> None:
        self.code_root = code_root
        self.code_funcs = code_funcs
        self.code_embeddings = []
        if not os.path.exists(BASE_PATH):
            os.makedirs(BASE_PATH)
        self.index_path = os.path.join(BASE_PATH, os.path.split(code_root)[1])

    def get_embedding(self, input_string):
        return get_embedding(input_string, engine='text-embedding-ada-002')

    def __compute_embeddings(self):
        cprint("Computing Embeddings on all Function snippets ...")
        if self.code_embeddings:
            return
        for code_func in self.code_funcs:
            code_func['relative_filepath'] = code_func['filepath'].replace(self.code_root, "")
            code_embedding = self.get_embedding(code_func["code"])
            self.code_embeddings.append(code_embedding)
    
    def create_index(self):
        cprint("Creating Nearest Neighbor Search Index on all Function Embeddings ...")
        self.index = nmslib.init(method='hnsw', space='cosinesimil')
        if os.path.exists(self.index_path):
            self.index.loadIndex(self.index_path, load_data=True)
        else:
            self.__compute_embeddings()
            self.index.addDataPointBatch(self.code_embeddings)
            self.index.createIndex({'post': 2}, print_progress=True)
            self.index.saveIndex(self.index_path, save_data=True)

    def search_index(self, query: str, num_neighbors: int = 3) -> Tuple[List[Dict[str, Any]], List[float]]:
        query_embedding = self.get_embedding(query)
        ids, distances = self.index.knnQuery(query_embedding, k=num_neighbors)
        code_funcs_neighbors = [
            self.code_funcs[i] for i in ids
        ]
        return code_funcs_neighbors, distances




    