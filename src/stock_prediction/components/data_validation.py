from stock_prediction.entity.config_entity import DataValidationConfig
import pandas as pd
import great_expectations as gx
from stock_prediction import logger

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
    
    def validate_data(self):
        try:
            data = pd.read_csv(self.config.raw_data_file, parse_dates=["Date"])
            columns = list(data.columns)
            context = gx.get_context()
            data_source = context.data_sources.add_pandas("stock_data_source")
            data_asset = data_source.add_dataframe_asset(name="stock_data_asset")
            batch_definition = data_asset.add_batch_definition_whole_dataframe("stock_data_batch")
            batch = batch_definition.get_batch(batch_parameters={"dataframe": data})
            suite = context.suites.add(
                gx.ExpectationSuite(self.config.ge_expectation_suite)
            )

            suite.add_expectation(
                gx.expectations.ExpectTableColumnsToMatchSet(
                    column_set=columns,
                    exact_match=True
                )
            )

            for column in columns:
                suite.add_expectation(
                    gx.expectations.ExpectColumnValuesToNotBeNull(
                        column=column
                    )
            )


            for column in columns:
                if column != "Date":
                    suite.add_expectation(
                        gx.expectations.ExpectColumnValuesToBeBetween(
                            column=column,
                            min_value=0
                            )
                        )
                    
            context.suites.add_or_update(suite)

            results = batch.validate(suite)
            validation_status = bool(results.success)
            self._write_status(validation_status)
            if validation_status:
                logger.info(f"Validation passed")
            else:
                logger.error(f"Data validation failed: {results}")
            return validation_status
        except Exception as e:
            logger.error(f"Error encountered during validation: {e}")
            raise e
    def _write_status(self, status: bool):
        with open(self.config.status_file, "w") as f:
            f.write(str(status))