from ..core.models import Component, ComponentType, PinType


def create_button(name: str) -> Component:
    """
    Cria um Component do tipo BUTTON.

    Botão precisa de um pino digital (INPUT ou INPUT_PULLUP) e não
    exige driver na V1.0.
    """
    return Component(
        name=name,
        component_type=ComponentType.BUTTON,
        required_pin_types=(PinType.DIGITAL,),
        requires_driver=False,
    )