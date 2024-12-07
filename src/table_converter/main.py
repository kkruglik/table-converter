import logging
import logging.config
import sys
from datetime import datetime
from pathlib import Path
from typing import Tuple

from table_converter.processors.bank_processors import BankStatementProcessor
from table_converter.utils import has_csv_or_xlsx_files
from table_converter.utils.utils import load_logging_config

logger = logging.getLogger("table_converter")


def setup_directories(run_id: str) -> Tuple[Path, Path]:
    base_data_dir = Path.cwd() / "data"
    input_dir = base_data_dir / "input"
    output_dir = base_data_dir / "output" / run_id

    for directory in [input_dir, output_dir]:
        if not directory.exists():
            logger.info(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)

    logger.info(f"Input directory: {input_dir}")
    logger.info(f"Output directory: {output_dir}")

    return input_dir, output_dir


def main():
    global logger
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    input_dir, output_dir = setup_directories(run_id)

    if not has_csv_or_xlsx_files(input_dir):
        msg = f"Input directory {input_dir} does not contain any CSV or XLSX files."
        logger.error(msg)
        raise FileNotFoundError(msg)

    try:
        log_filename = output_dir / "logs.log"

        logging_config = Path(__file__).parent / "config" / "logging.yaml"

        if not logging_config.exists():
            raise FileNotFoundError(f"Logging config file not found at {logging_config}")

        logging_config = load_logging_config(logging_config, {"log_filename": log_filename.as_posix()})
        logging.config.dictConfig(logging_config)

        logger.info(f"Running table processing with RUN ID: {run_id}")

        bank_processor = BankStatementProcessor()

        bank_processor.process_directory(input_dir)

        logger.info("Running post processing")

        bank_processor.post_process()

        logger.info("Saving results")

        bank_processor.save_output_statement(output_dir / "output_statement.csv")
        bank_processor.save_output_statement(output_dir / "output_statement.xlsx")

        logger.info(f"Converting finished successfully. Results saved to: {output_dir.absolute()}")
        sys.exit(0)

    except Exception as e:
        msg = f"Exception occurred: {e}"
        logger.error(msg)
        sys.exit(1)


if __name__ == '__main__':
    main()
