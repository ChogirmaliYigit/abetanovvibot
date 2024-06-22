from django.db.models import Manager


class BaseManager(Manager):
    def filter(self, *args, **kwargs):
        queryset = super().filter(*args, **kwargs)
        return queryset.filter(deleted_at__isnull=True)

    def all(self, *args, **kwargs):
        return self.filter()

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs, deleted_at__isnull=True)
