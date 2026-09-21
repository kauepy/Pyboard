from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PinType(Enum):
    """Tipos básicos de pinos que o PyBoard pode reconhecer."""
    DIGITAL = "digital"
    ANALOG = "analog"
    POWER = "power"
    GROUND = "ground"


class PinMode(Enum):
    """Modos de operação possíveis para um pino."""
    INPUT = "input"
    OUTPUT = "output"
    INPUT_PULLUP = "input_pullup"


class ComponentType(Enum):
    """Tipos de componentes suportados pelo PyBoard."""
    LED = "led"
    BUTTON = "button"
    MOTOR_DC = "motor_dc"
    SENSOR = "sensor"
    RELAY = "relay"
    OTHER = "other"


@dataclass(frozen=True)
class Pin:
    """
    Representa um pino de uma placa.

    frozen=True: pino não muda depois de criado, e passa a ser hashable
    (dá pra usar em set()/dict() pra controlar quais pinos já foram usados).
    """
    name: str
    pin_type: PinType
    number: Optional[int] = None
    supports_pwm: bool = False
    supports_i2c: bool = False
    supports_spi: bool = False
    supports_uart: bool = False

    def supports_mode(self, mode: PinMode) -> bool:
        """
        Deduz se o pino aceita um determinado PinMode a partir do pin_type,
        em vez de guardar supports_input/supports_output soltos (que na
        prática sempre coincidiam com DIGITAL/ANALOG).
        """
        if self.pin_type in (PinType.POWER, PinType.GROUND):
            return False
        return True


@dataclass
class Board:
    """Representa uma placa compatível com o PyBoard."""
    name: str
    manufacturer: str
    pins: list[Pin] = field(default_factory=list)
    voltage: float = 5.0

    def get_pin(self, name: str) -> Optional[Pin]:
        """Busca um pino pelo nome (ex.: 'D13')."""
        for pin in self.pins:
            if pin.name == name:
                return pin
        return None


@dataclass(frozen=True)
class Component:
    """
    Representa um componente eletrônico.

    frozen=True + tuple em required_pin_types: mesma lógica do Pin,
    fica hashable (list não é hashable, tuple é).
    """
    name: str
    component_type: ComponentType
    required_pin_types: tuple[PinType, ...] = field(default_factory=tuple)
    requires_driver: bool = False


@dataclass
class Connection:
    """Representa a conexão entre um componente e um pino."""
    component: Component
    pin: Pin
    mode: Optional[PinMode] = None