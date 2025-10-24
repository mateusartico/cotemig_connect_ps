from abc import ABC, abstractmethod
from app.models.entities import Usuario, Monitoria, Disciplina, Avaliacao, Suporte

class EntityFactory(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass

class UsuarioFactory(EntityFactory):
    def create(self, **kwargs):
        senha = kwargs.pop('senha', None)
        usuario = Usuario(**kwargs)
        if senha:
            usuario.set_password(senha)
        return usuario

class MonitoriaFactory(EntityFactory):
    def create(self, **kwargs):
        gerar_codigo = kwargs.pop('gerar_codigo', False)
        monitoria = Monitoria(**kwargs)
        if gerar_codigo:
            monitoria.gerar_codigo_presenca()
        return monitoria

class DisciplinaFactory(EntityFactory):
    def create(self, **kwargs):
        return Disciplina(**kwargs)

class AvaliacaoFactory(EntityFactory):
    def create(self, **kwargs):
        return Avaliacao(**kwargs)

class SuporteFactory(EntityFactory):
    def create(self, **kwargs):
        return Suporte(**kwargs)

class EntityFactoryProvider:
    _factories = {
        'usuario': UsuarioFactory(),
        'monitoria': MonitoriaFactory(),
        'disciplina': DisciplinaFactory(),
        'avaliacao': AvaliacaoFactory(),
        'suporte': SuporteFactory()
    }
    
    @classmethod
    def get_factory(cls, entity_type):
        factory = cls._factories.get(entity_type.lower())
        if not factory:
            raise ValueError(f"Factory não encontrada para tipo: {entity_type}")
        return factory
    
    @classmethod
    def create_entity(cls, entity_type, **kwargs):
        factory = cls.get_factory(entity_type)
        return factory.create(**kwargs)