from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups():
    from django.contrib.auth.models import Group
    group_name_list = ["Authors", "Editors", "Customers"]
    for group_name in group_name_list:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"The {group} group is created")


def merch_post_migration(sender, **kwargs):
    create_groups()

class MerchandisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'merchandises'

    def ready(self):
        post_migrate.connect(merch_post_migration, sender=self)
