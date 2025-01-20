import logging
from pathlib import Path

import numpy as np
import pandas as pd

from table_converter.processors.base import BankProcessor
from table_converter.utils.utils import find_skiprows, find_currency

logger = logging.getLogger(__name__)


class TBCProcessor(BankProcessor):
    def __init__(self):
        self.columns = {
            "payer_account",
            "date",
            "volume",
            "currency",
            "to_account",
            "bank_code",
            "message_for_beneficiary",
            "note",
            "type",
            "id_of_transaction",
        }

        self._column_dtypes = {
            "payer_account": "string",
            "date": "datetime64[ns]",
            "volume": "float64",
            "currency": "string",
            "to_account": "string",
            "bank_code": "string",
            "message_for_beneficiary": "string",
            "note": "string",
            "type": "string",
            "id_of_transaction": "string",
        }

        self._target_cols = {
            "payer_account": "Счёт",
            "date": "Дата",
            "volume": "Сумма",
            "volume_type": "Приход / расход",
            "currency": "Валюта",
            "note": "Комментарии",
            "id_of_transaction": "ID транзакции",
            "bank": "bank",  # service field
        }

    def _apply_dtypes(self, df) -> pd.DataFrame:
        return df.astype(self._column_dtypes)

    def _apply_features(self, df) -> pd.DataFrame:
        df["volume_type"] = np.where(df.volume > 0, "Приход", "Расход")
        df = df.sort_values(by=["date"], ascending=True)
        # df["date"] = df["date"].dt.strftime("%d.%m.%Y")
        df["bank"] = "TBC"
        df["volume"] = df["volume"].abs()
        return df

    def process(self, data: pd.DataFrame, currency: str = None) -> pd.DataFrame:
        data.columns = [self.normalize_string(i) for i in data.columns]
        df = self._apply_dtypes(data)
        df = self._apply_features(df)
        df = df.rename(columns=self._target_cols)
        df = df[list(self._target_cols.values())]
        return df

    def validate(self) -> bool:
        ...

    def is_bank_columns(self, input_columns: set) -> bool:
        return self.columns == self.normalize_columns(input_columns)


class BOGProcessor(BankProcessor):
    def __init__(self):
        self.columns = {
            "date",
            "doc_n",
            "debit",
            "credit",
            "recipient_name",
            "amount",
            "entry_comment",
            "nomination",
            "sender_account_n",
        }

        self._column_dtypes = {
            "date": "datetime64[ns]",
            "doc_n": "string",
            "debit": "float64",
            "credit": "float64",
            "recipient_name": "string",
            "nomination": "string",
        }

        self._target_cols = {
            "date": "Дата",
            "doc_n": "ID транзакции",
            "entry_comment": "Комментарии",
            "volume_type": "Приход / расход",
            "volume": "Сумма",
            "recipient_name": "Счёт получателя",
            "currency": "Валюта",
            "bank": "bank",
        }

    def _apply_dtypes(self, df) -> pd.DataFrame:
        return df.astype(self._column_dtypes)

    def _apply_features(self, df) -> pd.DataFrame:
        df["is_foreign_exchange"] = df["entry_comment"].str.contains("Foreign Exchange")
        df["volume_type"] = np.where(df.amount < 0, "Расход", "Приход")
        df["volume"] = df["credit"].fillna(df["debit"])
        df = df.sort_values(by=["date"], ascending=True)
        df["nomination"] = df["nomination"].str.replace("Conversion", "", regex=False)
        # df["date"] = df["date"].dt.strftime("%d.%m.%Y")
        df["bank"] = "BOG"
        df["volume"] = df["volume"].abs()
        return df

    def process(self, data: pd.DataFrame, currency: str = None) -> pd.DataFrame:
        data.columns = [self.normalize_string(i) for i in data.columns]
        df = self._apply_dtypes(data)
        df = self._apply_features(df)
        if currency:
            df["currency"] = currency
        else:
            logger.warning("No currency passed in BOGProcessor")
        df = df.rename(columns=self._target_cols)
        df = df[list(self._target_cols.values())]
        return df

    def validate(self) -> bool:
        pass

    def is_bank_columns(self, input_columns: set) -> bool:
        input_columns = self.normalize_columns(input_columns)
        return self.columns.issubset(input_columns)


class BankStatementFactory:
    def __init__(self):
        logger.debug("Initializing BankStatementFactory")
        self.processors = {
            "bog": BOGProcessor(),
            "tbc": TBCProcessor(),
        }
        logger.debug(f"Registered processors: {list(self.processors.keys())}")

    def identify_bank(self, data: pd.DataFrame) -> BankProcessor | None:
        logger.debug("Starting bank identification process")
        df_columns = set(data.columns)
        logger.debug(f"DataFrame columns: {df_columns}")

        for bank_name, processor in self.processors.items():
            logger.debug(f"Checking columns against {bank_name} processor")
            if processor.is_bank_columns(df_columns):
                logger.debug(f"Bank identified: {bank_name}")
                return processor

        logger.warning("No matching bank processor found for the given columns")
        return None


class BankStatementProcessor:
    def __init__(self):
        logger.debug("Initializing BankStatementProcessor")
        self.factory = BankStatementFactory()
        self.output_statement = pd.DataFrame()
        logger.debug("BankStatementProcessor initialized successfully")

    def process_statement(self, statement_filename: Path) -> pd.DataFrame:
        logger.debug(f"Starting to process statement: {statement_filename}")
        currency = None

        if not statement_filename.exists():
            msg = f"{statement_filename} does not exist"
            logger.error(msg)
            raise FileNotFoundError(msg)

        logger.debug(f"Reading file: {statement_filename}")
        if statement_filename.suffix == ".csv":
            logger.debug("Detected CSV file format")
            df = pd.read_csv(statement_filename, sep=';')
        elif statement_filename.suffix == ".xlsx":
            logger.debug("Detected Excel file format")
            skip_rows = find_skiprows(statement_filename, {"Date", "Doc N", "Loro Account"})
            logger.debug(f"Skip rows determined: {skip_rows}")
            currency = find_currency(statement_filename)
            logger.debug(f"Currency detected: {currency}")
            df = pd.read_excel(statement_filename, skiprows=skip_rows)
        else:
            logger.error(f"Unsupported file extension: {statement_filename.suffix}")
            raise ValueError(f"Unsupported file extension: {statement_filename.suffix}")

        logger.debug("Identifying bank processor")
        processor = self.factory.identify_bank(df)
        logger.debug(f"Bank processor identified: {processor.__class__.__name__}")

        try:
            logger.debug("Processing dataframe with identified processor")
            processed_df = processor.process(df, currency)
            logger.debug("Successfully processed statement")
            return processed_df
        except Exception as e:
            logger.error(f"Error while processing {statement_filename}: {e}")
            raise ValueError(f"Error while processing {statement_filename}: {e}")

    def process_directory(self, directory: Path) -> None:
        logger.debug(f"Starting to process directory: {directory}")

        statements_files = [i for i in directory.iterdir() if i.suffix in {".csv", ".xlsx"}]

        logger.info(f"Processing files: {statements_files}")

        for filename in statements_files:
            logger.info(f"Processing file {filename}")
            try:
                processed_statement_df = self.process_statement(filename)
                self.output_statement = pd.concat([self.output_statement, processed_statement_df],
                                                  ignore_index=True)
                logger.debug(f"Successfully processed CSV file: {filename}")
            except Exception as e:
                msg = f"Error processing CSV file {filename}: {str(e)}"
                logger.error(msg, exc_info=True)
                raise ValueError(msg)

        logger.info(f"Finished processing directory: {directory}")

    def post_process(self):
        try:
            logger.debug("Starting post-processing of output statement")
            logger.debug("Sorting values by date and bank")
            self.output_statement = self.output_statement.sort_values(by=["Дата", "bank", "ID транзакции", "Приход / расход"], ascending=[True, True, True, False])

            logger.debug("Formatting date column")
            self.output_statement["Дата"] = self.output_statement["Дата"].dt.strftime("%d.%m.%Y")

            logger.debug("Setting multi-index")
            self.output_statement = self.output_statement.set_index(["ID транзакции", "Дата"])
            logger.debug("Post-processing completed successfully")
        except Exception as e:
            msg = f"Error processing output statement {str(e)}"
            logger.error(msg, exc_info=True)
            raise ValueError(msg)

    def save_output_statement(self, filename: Path) -> None:
        logger.debug(f"Saving output statement to: {filename}")

        if filename.suffix == ".csv":
            logger.debug("Saving as CSV with comma decimal separator and semicolon delimiter")
            self.output_statement.to_csv(filename, decimal=",", sep=";", index=True)

        elif filename.suffix == ".xlsx":
            logger.debug("Saving as Excel file")
            logger.debug("Converting decimal points to commas in 'Сумма' column")
            self.output_statement["Сумма"] = self.output_statement["Сумма"].astype(str).str.replace(".", ",")
            self.output_statement.to_excel(filename, index=True)

        logger.debug(f"Successfully saved output statement to: {filename}")
