"""
Padrão Strategy para diferentes algoritmos de busca e validação
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import re

class SearchStrategy(ABC):
    """Interface para estratégias de busca"""
    
    @abstractmethod
    def search(self, query: str, items: List[Any]) -> List[Any]:
        pass

class TitleSearchStrategy(SearchStrategy):
    """Estratégia de busca por título"""
    
    def search(self, query: str, items: List[Any]) -> List[Any]:
        query_lower = query.lower()
        return [item for item in items if query_lower in item.titulo.lower()]

class DescriptionSearchStrategy(SearchStrategy):
    """Estratégia de busca por descrição"""
    
    def search(self, query: str, items: List[Any]) -> List[Any]:
        query_lower = query.lower()
        return [item for item in items 
                if item.descricao and query_lower in item.descricao.lower()]

class TagSearchStrategy(SearchStrategy):
    """Estratégia de busca por tags"""
    
    def search(self, query: str, items: List[Any]) -> List[Any]:
        query_lower = query.lower()
        return [item for item in items 
                if item.tags and query_lower in item.tags.lower()]

class FullTextSearchStrategy(SearchStrategy):
    """Estratégia de busca em texto completo"""
    
    def search(self, query: str, items: List[Any]) -> List[Any]:
        query_lower = query.lower()
        results = []
        
        for item in items:
            # Busca no título
            if query_lower in item.titulo.lower():
                results.append(item)
                continue
            
            # Busca na descrição
            if item.descricao and query_lower in item.descricao.lower():
                results.append(item)
                continue
            
            # Busca nas tags
            if item.tags and query_lower in item.tags.lower():
                results.append(item)
        
        return results

class ValidationStrategy(ABC):
    """Interface para estratégias de validação"""
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        pass

class EmailValidationStrategy(ValidationStrategy):
    """Estratégia de validação de email"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}
        email = data.get('email', '')
        tipo = data.get('tipo', '')
        
        if not email:
            errors['email'] = ['Email é obrigatório']
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            errors['email'] = ['Email inválido']
        elif tipo == 'aluno' and not email.endswith('@aluno.cotemig.com.br'):
            errors['email'] = ['Email deve ser @aluno.cotemig.com.br para alunos']
        elif tipo == 'monitor' and not email.endswith('@cotemig.com.br'):
            errors['email'] = ['Email deve ser @cotemig.com.br para monitores']
        
        return errors

class PasswordValidationStrategy(ValidationStrategy):
    """Estratégia de validação de senha"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}
        senha = data.get('senha', '')
        
        if not senha:
            errors['senha'] = ['Senha é obrigatória']
        elif len(senha) < 8:
            errors['senha'] = ['Senha deve ter pelo menos 8 caracteres']
        elif not re.search(r'[A-Za-z]', senha):
            errors['senha'] = ['Senha deve conter pelo menos uma letra']
        elif not re.search(r'\d', senha):
            errors['senha'] = ['Senha deve conter pelo menos um número']
        
        return errors

class MonitoriaValidationStrategy(ValidationStrategy):
    """Estratégia de validação de monitoria"""
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        errors = {}
        
        if not data.get('titulo'):
            errors['titulo'] = ['Título é obrigatório']
        
        if not data.get('data_hora'):
            errors['data_hora'] = ['Data e hora são obrigatórias']
        
        vagas = data.get('vagas_total', 0)
        if not isinstance(vagas, int) or vagas <= 0:
            errors['vagas_total'] = ['Número de vagas deve ser maior que zero']
        
        return errors

class SearchContext:
    """Context para estratégias de busca"""
    
    def __init__(self, strategy: SearchStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SearchStrategy):
        self._strategy = strategy
    
    def execute_search(self, query: str, items: List[Any]) -> List[Any]:
        return self._strategy.search(query, items)

class ValidationContext:
    """Context para estratégias de validação"""
    
    def __init__(self):
        self._strategies = []
    
    def add_strategy(self, strategy: ValidationStrategy):
        self._strategies.append(strategy)
    
    def validate(self, data: Dict[str, Any]) -> Dict[str, List[str]]:
        all_errors = {}
        
        for strategy in self._strategies:
            errors = strategy.validate(data)
            for field, field_errors in errors.items():
                if field not in all_errors:
                    all_errors[field] = []
                all_errors[field].extend(field_errors)
        
        return all_errors