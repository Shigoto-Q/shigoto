class BaseInstructionsError(Exception):
    """
    Base class for all instructions related exceptions.
    """


class InstructionsInvalidParameterError(BaseInstructionsError):
    pass


class InstructionsMissingParameterError(BaseInstructionsError):
    pass


class InstructionsInvalidYamlFileError(BaseInstructionsError):
    pass
