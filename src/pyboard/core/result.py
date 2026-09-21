from dataclasses import dataclass, field
from typing import Any, Optional

from errors import PyBoardError


@dataclass
class ValidationResult:
    """
    Resultado de uma validação completa (validate_all).
    Em vez de parar no primeiro erro, acumula todos os problemas
    encontrados pra reportar de uma vez só.
    """
    errors: list[PyBoardError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, error: PyBoardError) -> None:
        self.errors.append(error)

    def raise_if_invalid(self) -> None:
        """Levanta o primeiro erro encontrado, se houver algum."""
        if self.errors:
            raise self.errors[0]


@dataclass
class Result:
    """
    Resultado genérico de uma etapa do pipeline (parse, compile, upload...).
    success=True -> usa 'value'. success=False -> usa 'error'.
    """
    success: bool
    value: Optional[Any] = None
    error: Optional[PyBoardError] = None

    @classmethod
    def ok(cls, value: Any = None) -> "Result":
        return cls(success=True, value=value)

    @classmethod
    def fail(cls, error: PyBoardError) -> "Result":
        return cls(success=False, error=error)