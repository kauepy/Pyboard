class PyBoardError(Exception):
    """Classe base pra todos os erros do core do PyBoard."""


class PinError(PyBoardError):
    """Classe base pra erros relacionados a pinos."""


class PinTypeMismatchError(PinError):
    """Levantado quando o tipo do pino não é compatível com o componente."""


class PinModeNotSupportedError(PinError):
    """Levantado quando o pino não suporta o PinMode pedido."""


class PinNotInBoardError(PinError):
    """Levantado quando o pino informado não pertence à placa."""


class PinAlreadyUsedError(PinError):
    """Levantado quando o mesmo pino é usado em mais de uma conexão."""


class ComponentError(PyBoardError):
    """Classe base pra erros relacionados a componentes."""


class DriverNotFoundError(ComponentError):
    """Levantado quando um componente exige driver e nenhum foi encontrado."""