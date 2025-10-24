from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from app.core.database_singleton import db

class IRepository(ABC):
    @abstractmethod
    def create(self, **kwargs):
        pass
    
    @abstractmethod
    def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    def get_all(self) -> List:
        pass
    
    @abstractmethod
    def update(self, instance, **kwargs):
        pass
    
    @abstractmethod
    def delete(self, instance):
        pass
    
    @abstractmethod
    def save(self, instance):
        pass

class BaseRepository(IRepository):
    def __init__(self, model):
        self.model = model
    
    def create(self, **kwargs):
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_by_id(self, id: int):
        return self.model.query.get(id)
    
    def get_all(self) -> List:
        return self.model.query.all()
    
    def find_by(self, **kwargs) -> List:
        return self.model.query.filter_by(**kwargs).all()
    
    def find_one_by(self, **kwargs) -> Optional:
        return self.model.query.filter_by(**kwargs).first()
    
    def update(self, instance, **kwargs):
        try:
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self, instance):
        try:
            db.session.delete(instance)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    
    def save(self, instance):
        try:
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as e:
            db.session.rollback()
            raise e
    
    def count(self) -> int:
        return self.model.query.count()
    
    def exists(self, **kwargs) -> bool:
        return self.model.query.filter_by(**kwargs).first() is not None
    
    def paginate(self, page: int = 1, per_page: int = 10, **filters):
        query = self.model.query
        if filters:
            query = query.filter_by(**filters)
        return query.paginate(page=page, per_page=per_page, error_out=False)