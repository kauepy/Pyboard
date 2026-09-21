from ..core.models import Component, ComponentType, PinType


def create_led(name: str) -> Component:
    """
    Cria um Component do tipo LED.

    LED precisa de um pino digital (liga/desliga ou PWM pra brilho) e
    não exige driver na V1.0.
    """
    return Component(
        name=name,
        component_type=ComponentType.LED,
        required_pin_types=(PinType.DIGITAL,),
        requires_driver=False,
    )