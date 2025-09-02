from typing import List, Optional
from app.repositories.base_repository import BaseRepository
from app.models.entities import Disciplina, Monitor

class DisciplinaRepository(BaseRepository):
    """Repositório para operações com disciplinas"""
    
    def __init__(self):
        super().__init__(Disciplina)
    
    def get_by_codigo(self, codigo: str) -> Optional[Disciplina]:
        """Busca disciplina por código"""
        return self.find_one_by(codigo=codigo, ativo=True)
    
    def get_by_curso(self, curso_id: int) -> List[Disciplina]:
        """Busca disciplinas por curso"""
        return self.find_by(curso_id=curso_id, ativo=True)
    
    def get_by_professor(self, professor_id: int) -> List[Disciplina]:
        """Busca disciplinas por professor"""
        return self.find_by(professor_id=professor_id, ativo=True)
    
    def get_com_monitores(self) -> List[Disciplina]:
        """Retorna disciplinas que possuem monitores ativos"""
        return self.model_class.query.join(Monitor)\
            .filter(Monitor.ativo == True, self.model_class.ativo == True)\
            .distinct().all()
    
    def get_sem_monitores(self) -> List[Disciplina]:
        """Retorna disciplinas que não possuem monitores"""
        disciplinas_com_monitores = self.model_class.query.join(Monitor)\
            .filter(Monitor.ativo == True).distinct().subquery()
        
        return self.model_class.query.filter(
            ~self.model_class.id.in_(disciplinas_com_monitores.select()),
            self.model_class.ativo == True
        ).all()
    
    def search_by_name(self, nome: str) -> List[Disciplina]:
        """Busca disciplinas por nome (busca parcial)"""
        return self.model_class.query.filter(
            self.model_class.nome.ilike(f'%{nome}%'),
            self.model_class.ativo == True
        ).all()