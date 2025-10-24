"""
Padrão Observer para notificações do sistema
"""
from abc import ABC, abstractmethod
from typing import List, Any

class Observer(ABC):
    """Interface para observadores"""
    
    @abstractmethod
    def update(self, subject, event_type: str, data: Any = None):
        pass

class Subject(ABC):
    """Classe base para objetos observáveis"""
    
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Adiciona um observador"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Remove um observador"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event_type: str, data: Any = None):
        """Notifica todos os observadores"""
        for observer in self._observers:
            observer.update(self, event_type, data)

class NotificationObserver(Observer):
    """Observador para notificações gerais"""
    
    def __init__(self, name: str):
        self.name = name
        self.notifications = []
    
    def update(self, subject, event_type: str, data: Any = None):
        notification = {
            'type': event_type,
            'data': data,
            'timestamp': __import__('datetime').datetime.now()
        }
        self.notifications.append(notification)
        print(f"[{self.name}] Notificação: {event_type} - {data}")

class EmailObserver(Observer):
    """Observador para envio de emails"""
    
    def update(self, subject, event_type: str, data: Any = None):
        if event_type in ['usuario_cadastrado', 'monitoria_criada', 'avaliacao_criada']:
            self._send_email(event_type, data)
    
    def _send_email(self, event_type: str, data: Any):
        # Simulação de envio de email
        print(f"Email enviado: {event_type} - {data}")

class MonitoriaSubject(Subject):
    """Subject para eventos de monitoria"""
    
    def criar_monitoria(self, monitoria_data):
        # Lógica de criação
        self.notify('monitoria_criada', monitoria_data)
    
    def cancelar_monitoria(self, monitoria_id):
        # Lógica de cancelamento
        self.notify('monitoria_cancelada', {'id': monitoria_id})
    
    def finalizar_monitoria(self, monitoria_id):
        # Lógica de finalização
        self.notify('monitoria_finalizada', {'id': monitoria_id})

# Instância global do subject de monitoria
monitoria_subject = MonitoriaSubject()

# Configuração dos observadores
notification_observer = NotificationObserver("Sistema")
email_observer = EmailObserver()

monitoria_subject.attach(notification_observer)
monitoria_subject.attach(email_observer)