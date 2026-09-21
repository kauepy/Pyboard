from models import Board, Component, Connection, Pin, PinMode
from errors import (
    PinError,
    PinTypeMismatchError,
    PinModeNotSupportedError,
    PinNotInBoardError,
    PinAlreadyUsedError,
    ComponentError,
    DriverNotFoundError,
)
from result import ValidationResult


def validate_pin_type(component: Component, pin: Pin) -> None:
    """Confere se o tipo do pino é um dos tipos exigidos pelo componente."""
    if pin.pin_type not in component.required_pin_types:
        raise PinTypeMismatchError(
            f"Pino '{pin.name}' ({pin.pin_type.value}) não é compatível com "
            f"'{component.name}' (esperado: "
            f"{[t.value for t in component.required_pin_types]})"
        )


def validate_pin_mode(pin: Pin, mode: PinMode | None) -> None:
    """Confere se o pino aceita o modo pedido na conexão."""
    if mode is not None and not pin.supports_mode(mode):
        raise PinModeNotSupportedError(
            f"Pino '{pin.name}' ({pin.pin_type.value}) não suporta o modo "
            f"'{mode.value}'"
        )


def validate_pin_belongs_to_board(board: Board, pin: Pin) -> None:
    """Confere se o pino realmente existe na placa informada."""
    if pin not in board.pins:
        raise PinNotInBoardError(
            f"Pino '{pin.name}' não pertence à placa '{board.name}'"
        )


def validate_pin_uniqueness(connections: list[Connection]) -> None:
    """
    Confere se nenhum pino está sendo usado em mais de uma conexão.
    Usa set() porque Pin agora é frozen (hashable).
    """
    used_pins: set[Pin] = set()
    for conn in connections:
        if conn.pin in used_pins:
            raise PinAlreadyUsedError(
                f"Pino '{conn.pin.name}' já está sendo usado em outra conexão"
            )
        used_pins.add(conn.pin)


def validate_driver_availability(component: Component) -> None:
    """
    Confere se o componente exige driver. Na V1.0 não existe sistema de
    drivers ainda (isso só chega na V3.0), então qualquer componente com
    requires_driver=True falha aqui por enquanto.
    """
    if component.requires_driver:
        raise DriverNotFoundError(
            f"'{component.name}' exige driver, mas o sistema de drivers "
            f"ainda não existe (previsto pra V3.0)"
        )


def validate_connection(connection: Connection, board: Board) -> None:
    """Roda todas as checagens de uma única conexão."""
    validate_pin_belongs_to_board(board, connection.pin)
    validate_pin_type(connection.component, connection.pin)
    validate_pin_mode(connection.pin, connection.mode)
    validate_driver_availability(connection.component)


def validate_all(board: Board, connections: list[Connection]) -> ValidationResult:
    """
    Roda a validação completa de todas as conexões de um projeto e
    devolve um ValidationResult com TODOS os erros encontrados, sem
    parar no primeiro.
    """
    result = ValidationResult()

    try:
        validate_pin_uniqueness(connections)
    except PinError as e:
        result.add_error(e)

    for conn in connections:
        try:
            validate_connection(conn, board)
        except (PinError, ComponentError) as e:
            result.add_error(e)

    return result