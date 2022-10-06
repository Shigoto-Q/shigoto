import logging

import yaml

from services.horizon.instructions import constants
from services.horizon.instructions import exceptions


_LOG_PREFIX = "[INSTRUCTIONS-PARSER]"
logger = logging.getLogger(__name__)


class InstructionParser:
    def __init__(self, instructions_file_path):
        self.instructions_file_path = instructions_file_path
        self.instructions_file = None
        self._open_yaml()
        self._validate_keys()
        self._validate_summary()
        self._validate_project_params()

    def _open_yaml(self):
        with open(self.instructions_file_path) as f:
            self.instructions_file = yaml.load(f, yaml.FullLoader)

    def _validate_keys(self):
        additional_fields = [
            field
            for field in self.instructions_file.keys()
            if field not in constants.INSTRUCTION_FILE_ALLOWED_FIELDS
        ]
        missing_fields = [
            field
            for field in constants.INSTRUCTION_FILE_ALLOWED_FIELDS
            if field not in self.instructions_file.keys()
        ]
        if missing_fields:
            raise exceptions.InstructionsInvalidYamlFileError(
                f'The instructions file is missing the following keys: {", ".join(missing_fields)}!'
            )
        if additional_fields:
            raise exceptions.InstructionsInvalidYamlFileError(
                f'The instructions file contains additional invalid keys: {", ".join(additional_fields)}!'
            )

    def _validate_summary(self):
        summary = self.instructions_file.get("summary", {})
        language = summary.get("language")
        framework = summary.get("framework")
        if language is None:
            raise exceptions.InstructionsMissingParameterError(
                f"{_LOG_PREFIX} Missing language parameter!"
            )
        if language not in constants.ALLOWED_LANGUAGES:
            raise exceptions.InstructionsInvalidParameterError(
                f"{_LOG_PREFIX} Invalid language - {language} provided."
            )
        if framework not in constants.ALLOWED_FRAMEWORKS.get(language):
            raise exceptions.InstructionsInvalidParameterError(
                f"{_LOG_PREFIX} Invalid framework provided!"
            )

    def _validate_project_params(self):
        project = self.instructions_file.get("project", {})
        if project.get("name") is None:
            raise exceptions.InstructionsMissingParameterError(
                f"{_LOG_PREFIX} Missing name parameter!"
            )
        if project.get("source") is None:
            raise exceptions.InstructionsMissingParameterError(
                f"{_LOG_PREFIX} Missing source parameter!"
            )

    @property
    def summary(self):
        return self.instructions_file.get("summary")

    @property
    def project(self):
        return self.instructions_file.get("project")
