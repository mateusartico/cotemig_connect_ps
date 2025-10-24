"""
Padrão Factory Method para criação de objetos do domínio
"""
from abc import ABC, abstractmethod
from app.models.entities import Usuario, Monitoria, Disciplina, Avaliacao, Suporte

class EntityFactory(ABC):
    """Factory abstrata para criação de entidades"""
    
    @abstractmethod
    def create(self, **kwargs):
        pass

class UsuarioFactory(EntityFactory):
    """Factory para criação de usuários"""
    
    def create(self, **kwargs):
        senha = kwargs.pop('senha', None)
        usuario = Usuario(**kwargs)
        if senha:
            usuario.set_password(senha)
        return usuario

class MonitoriaFactory(EntityFactory):
    """Factory para criação de monitorias"""
    
    def create(self, **kwargs):
        monitoria = Monitoria(**kwargs)
        if kwargs.get('gerar_codigo', False):
            monitoria.gerar_codigo_presenca()
        return monitoria

class DisciplinaFactory(EntityFactory):
    """Factory para criação de disciplinas"""
    
    def create(self, **kwargs):
        return Disciplina(**kwargs)

class AvaliacaoFactory(EntityFactory):
    """Factory para criação de avaliações"""
    
    def create(self, **kwargs):
        return Avaliacao(**kwargs)

class SuporteFactory(EntityFactory):
    """Factory para criação de tickets de suporte"""
    
    def create(self, **kwargs):
        return Suporte(**kwargs)

class EntityFactoryProvider:
    """Provedor de factories - Padrão Factory Method"""
    
    _factories = {
        'usuario': UsuarioFactory(),
        'monitoria': MonitoriaFactory(),
        'disciplina': DisciplinaFactory(),
        'avaliacao': AvaliacaoFactory(),
        'suporte': SuporteFactory()
    }
    
    @classmethod
    def get_factory(cls, entity_type):
        """Retorna a factory apropriada para o tipo de entidade"""
        factory = cls._factories.get(entity_type.lower())
        if not factory:
            raise ValueError(f"Factory não encontrada para tipo: {entity_type}")
        return factory
    
    @classmethod
    def create_entity(cls, entity_type, **kwargs):
        """Cria uma entidade usando a factory apropriada"""
        factory = cls.get_factory(entity_type)
        return factory.create(**kwargs)