from ..core.models import Component, ComponentType, PinType


def create_motor_dc(name: str) -> Component:
    """
    Cria um Component do tipo MOTOR_DC.

    Motor DC não liga direto num pino digital comum — precisa de um
    driver (tipo L298N/L293D) pra lidar com a corrente. required_pin_types
    aqui é o pino de controle (PWM pra velocidade), não a alimentação do
    motor em si.

    requires_driver=True: o sistema de drivers só chega na V3.0, então por
    enquanto validar/compilar um projeto com motor deve falhar até lá
    (é o DriverNotFoundError que já deixamos pronto no errors.py).
    """
    return Component(
        name=name,
        component_type=ComponentType.MOTOR_DC,
        required_pin_types=(PinType.DIGITAL,),
        requires_driver=True,
    )