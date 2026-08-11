from stock_prediction.entity.config_entity import DataValidationConfig
import pandas as pd
import great_expectations as gx
from stock_prediction import logger

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
    def _get_or_create_data_sources(self, context, name):
        try:
            return context.data_sources.get(name)
        except Exception:
            logger.info(f"Data sourcess '{name}' not found, creating it..")
            return context.data_sources.add_pandas(name)
    def _get_or_create_asset(self, data_source, name):
        try:
            return data_source.get_asset(name=name)
        except Exception:
            logger.info(f"Data asset '{name}' not found, creating it..")
            return data_source.add_dataframe_asset(name=name)
    def _get_or_create_batch_definition(self, data_asset, name):
        try:
            return data_asset.get_batch_definition_name(name)
        except Exception:
            logger.info(f"Batch definition '{name}' not found, creating it..")
            return data_asset.add_batch_definition_whole_dataframe(name)
        
    
    def validate_data(self):
        try:
            data = pd.read_csv(self.config.raw_data_file)
            columns = list(data.columns)
            context = gx.get_context(mode="file", project_root_dir=".")
            

            data_source = self._get_or_create_data_sources(context, name="stock_data_source")
            data_asset = self._get_or_create_asset(data_source=data_source, name="stock_data_asset")
            batch_definition = self._get_or_create_batch_definition(data_asset=data_asset, name="stock_data_batch")
            # batch = batch_definition.get_batch(batch_parameters={"dataframe": data})
            
            
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
                if column != "date":
                    suite.add_expectation(
                        gx.expectations.ExpectColumnValuesToBeBetween(
                            column=column,
                            min_value=0
                            )
                        )
                    
            context.suites.add_or_update(suite)
            validation_definition = context.validation_definitions.add_or_update(
                gx.ValidationDefinition(
                    name="stock_data_validation_definition",
                    data=batch_definition,
                    suite=suite
                )
            )
            checkpoint = context.checkpoints.add_or_update(
                gx.Checkpoint(
                    name="stock_data_checkpoint",
                    validation_definitions=[validation_definition],
                    result_format="SUMMARY"
                )
            )
            checkpoint_result = checkpoint.run(
                batch_parameters={"dataframe": data}
            )
            validation_status = bool(checkpoint_result.success)
            context.build_data_docs()
            # results = batch.validate(suite)
            # validation_status = bool(results.success)
            self._write_status(validation_status)
            if validation_status:
                logger.info(f"Validation passed")
            else:
                logger.error(f"Data validation failed: {validation_status}")
            return validation_status
        except Exception as e:
            logger.error(f"Error encountered during validation: {e}")
            raise e
    def _write_status(self, status: bool):
        with open(self.config.status_file, "w") as f:
            f.write(str(status))
            
            
class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def _get_or_create_data_source(self, context, name):
        try:
            return context.data_sources.get(name)
        except Exception:
            logger.info(f"Data source '{name}' not found, creating it")
            return context.data_sources.add_pandas(name)

    def _get_or_create_data_asset(self, data_source, name):
        try:
            return data_source.get_asset(name=name)
        except Exception:
            logger.info(f"Data asset '{name}' not found, creating it")
            return data_source.add_dataframe_asset(name=name)

    def _get_or_create_batch_definition(self, data_asset, name):
        try:
            return data_asset.get_batch_definition(name)
        except Exception:
            logger.info(f"Batch definition '{name}' not found, creating it")
            return data_asset.add_batch_definition_whole_dataframe(name)

    def validate_data(self):
        try:
            data = pd.read_csv(self.config.raw_data_file)
            columns = list(data.columns)
            context = gx.get_context(mode="file", project_root_dir=".")

            # ---- get-or-create every GE object, so this works whether
            # ---- this is the first run ever, or the 100th rerun ----
            data_source = self._get_or_create_data_source(context, "stock_data_source")
            data_asset = self._get_or_create_data_asset(data_source, "stock_data_asset")
            batch_definition = self._get_or_create_batch_definition(data_asset, "stock_data_batch")
            batch = batch_definition.get_batch(batch_parameters={"dataframe": data})

            # suite: add_or_update handles both "doesn't exist yet" and "already exists"
            suite = context.suites.add_or_update(
                gx.ExpectationSuite(name=self.config.ge_expectation_suite)
            )
            # clear out any expectations from a previous run so they don't pile up duplicated
            suite.expectations = []

            suite.add_expectation(
                gx.expectations.ExpectTableColumnsToMatchSet(
                    column_set=columns,
                    exact_match=True
                )
            )

            for column in columns:
                suite.add_expectation(
                    gx.expectations.ExpectColumnValuesToNotBeNull(column=column)
                )

            for column in columns:
                if column != "date":
                    suite.add_expectation(
                        gx.expectations.ExpectColumnValuesToBeBetween(
                            column=column,
                            min_value=0
                        )
                    )

            context.suites.add_or_update(suite)

            validation_definition = context.validation_definitions.add_or_update(
                gx.ValidationDefinition(
                    name="stock_data_validation_definition",
                    data=batch_definition,
                    suite=suite
                )
            )

            checkpoint = context.checkpoints.add_or_update(
                gx.Checkpoint(
                    name="stock_data_checkpoint",
                    validation_definitions=[validation_definition],
                    result_format="SUMMARY"
                )
            )

            checkpoint_result = checkpoint.run(
                batch_parameters={"dataframe": data}
            )
            validation_status = bool(checkpoint_result.success)
            context.build_data_docs()

            self._write_status(validation_status)
            if validation_status:
                logger.info("Validation passed")
            else:
                logger.error(f"Data validation failed: {validation_status}")
            return validation_status

        except Exception as e:
            logger.error(f"Error encountered during validation: {e}")
            raise e

    def _write_status(self, status: bool):
        with open(self.config.status_file, "w") as f:
            f.write(str(status))