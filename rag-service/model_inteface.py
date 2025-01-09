import numpy as np


class Model:

    def get_device(self) -> str:
        pass

    def embed(self, document: str) -> np.ndarray:
        pass

    def embed_batch(self, documents: list[str]) -> np.ndarray:
        pass