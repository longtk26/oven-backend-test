from django.db.models import Model, Q
from django.core.exceptions import ValidationError


class BaseRepository:
    def __init__(self, model: Model):
        self.model = model

    def create(self, data) -> Model:
        return self.model.objects.create(**data)

    def create_many(self, data_list) -> list[Model]:
        instances = [self.model(**data) for data in data_list]
        return self.model.objects.bulk_create(instances)
    
    def find_one(self, **filters) -> Model | None:
        try:
            return self.model.objects.get(**filters)
        except self.model.DoesNotExist:
            return None
        except ValidationError:
            return None
        
    def find_many(self, **filters) -> list[Model]:
        try:
            return self.model.objects.filter(**filters)
        except ValidationError:
            return []

    def update(self, filters, data):
        try:
            return self.model.objects.filter(**filters).update(**data)
        except ValidationError:
            return None

    def soft_delete(self, **filters):
        try:
            return self.model.objects.filter(**filters).update(is_deleted=True)
        except ValidationError:
            return None
    
    def delete(self, **filters):
        try:
            return self.model.objects.filter(**filters).delete()
        except ValidationError:
            return None

    def paginate(self, page=1, limit=10, order_by='created_at', search=None, search_fields=None, **filters):
        """
        Paginate with optional ordering and keyword search.
        Args:
            page (int): page number
            limit (int): number of items per page
            order_by (str or list): e.g. "-created_at" or ["name", "-price"]
            search (str): keyword to search for
            search_fields (list): fields to search in, e.g. ["name", "description"]
            filters (dict): filters passed as kwargs
        """
        queryset = self.model.objects.filter(**filters)

        # 🔍 Apply search if provided
        if search and search_fields:
            q_objects = Q()
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search})
            queryset = queryset.filter(q_objects)

        # 🧭 Apply ordering if provided
        if order_by:
            if isinstance(order_by, list):
                queryset = queryset.order_by(*order_by)
            else:
                queryset = queryset.order_by(order_by)

        # 📄 Pagination logic
        count = queryset.count()
        total_pages = (count + limit - 1) // limit
        offset = (page - 1) * limit
        data = queryset[offset:offset + limit]

        return data, count, total_pages