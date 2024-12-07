from abc import ABC, abstractmethod

import pandas as pd


class BankProcessor(ABC):

    @abstractmethod
    def process(self, data: pd.DataFrame, currency: str = None) -> pd.DataFrame:
        pass

    @abstractmethod
    def validate(self) -> bool:
        pass

    @abstractmethod
    def is_bank_columns(self, columns: set) -> bool:
        pass

    @staticmethod
    def normalize_string(input_string: str) -> str:
        return input_string.lower() \
                    .strip() \
                    .replace(' ', '_') \
                    .replace('-', '_') \
                    .replace(' ', '_') \
                    .translate(str.maketrans('', '', '(),.'))

    def normalize_columns(self, input_set) -> set:
        normalized = set()
        for item in input_set:
            if isinstance(item, str):
                normalized_item = self.normalize_string(item)
                normalized.add(normalized_item)
        return normalized
