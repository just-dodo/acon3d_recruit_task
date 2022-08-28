from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_groups():
    from django.contrib.auth.models import Group
    group_name_list = ["Authors", "Editors", "Customers"]
    for group_name in group_name_list:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"The {group} group is created")


def set_group_permission():

    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import Merchandise, MerchContent

    authors_group = Group.objects.get(name="Authors")
    editors_group = Group.objects.get(name="Editors")
    users_group = Group.objects.get(name="Customers")

    # print(Permission.objects.all())
    merchandise_content_type = ContentType.objects.get_for_model(Merchandise)
    merchcontent_content_type = ContentType.objects.get_for_model(MerchContent)

    merch_permissions = Permission.objects.filter(
        content_type=merchandise_content_type,
    )
    merchcontent_permissions = Permission.objects.filter(
        content_type=merchcontent_content_type,
    )

    add_merch_permission = merch_permissions.get(codename="add_merchandise")
    add_merchcontent_permission = merchcontent_permissions.get(
        codename="add_merchcontent")
    authors_group.permissions.add(add_merch_permission)
    authors_group.permissions.add(add_merchcontent_permission)

    editors_group.permissions.set(
        list(merch_permissions)+list(merchcontent_permissions))

def merch_post_migration(sender, **kwargs):
    create_groups()
    set_group_permission()

class MerchandisesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'merchandises'

    def ready(self):
        post_migrate.connect(merch_post_migration, sender=self)
