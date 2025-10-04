from django.db.models import Model


class BaseRepository:
    def __init__(self, model: Model):
        self.model = model

    def create(self, data):
        return self.model.objects.create(**data)

    def create_many(self, data_list):
        instances = [self.model(**data) for data in data_list]
        return self.model.objects.bulk_create(instances)
    
    def find_one(self, **filters):
        try:
            return self.model.objects.get(**filters)
        except self.model.DoesNotExist:
            return None
        
    def find_many(self, **filters):
        return self.model.objects.filter(**filters)
    
    def update(self, filters, data):
        return self.model.objects.filter(**filters).update(**data)
    
    def soft_delete(self, **filters):
        return self.model.objects.filter(**filters).update(is_deleted=True)
    
    def delete(self, **filters):
        return self.model.objects.filter(**filters).delete()
    
    def paginate(self, page=1, limit=10, **filters):
        offset = (page - 1) * limit
        return self.model.objects.filter(**filters)[offset:offset + limit]