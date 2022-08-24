from django.contrib.auth.models import Group


def post_migration():
    group_name_list = ["Authors", "Editors", "Customers"]
    for group_name in group_name_list:
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"The {group} group is created")
