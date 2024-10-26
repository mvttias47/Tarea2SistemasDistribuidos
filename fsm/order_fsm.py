from transitions import Machine

class OrderFSM:
    states = ['Procesando', 'Preparación', 'Enviado', 'Entregado', 'Finalizado']

    def __init__(self, order):
        self.order = order
        self.machine = Machine(model=self, states=OrderFSM.states, initial='Procesando')
        
        # Definir las transiciones de estado
        self.machine.add_transition(trigger='preparar', source='Procesando', dest='Preparación')
        self.machine.add_transition(trigger='enviar', source='Preparación', dest='Enviado')
        self.machine.add_transition(trigger='entregar', source='Enviado', dest='Entregado')
        self.machine.add_transition(trigger='finalizar', source='Entregado', dest='Finalizado')

    def get_order_status(self):
        return self.state
