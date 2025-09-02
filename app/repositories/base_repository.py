from app import db

class BaseRepository:
    def __init__(self, model):
        self.model = model
    
    def create(self, **kwargs):
        instance = self.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
    
    def get_by_id(self, id):
        return self.model.query.get(id)
    
    def get_all(self):
        return self.model.query.all()
    
    def update(self, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance
    
    def delete(self, instance):
        db.session.delete(instance)
        db.session.commit()
    
    def save(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance