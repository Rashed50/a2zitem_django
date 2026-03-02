from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    if sender.name != "users":
        return

    users_data = [
        # 1️⃣ Superuser
        {
            "email"             : "superuser@test.com",
            "phone"             : "+8801500000001",
            "password"          : "123456ra",
            "first_name"        : "Mr.",
            "last_name"         : "Superuser",
            "is_active"         : True,
            "is_superuser"      : True,
            "is_admin"          : True,
            "is_email_verified" : True,
            "is_phone_verified" : True,
            "group"             : "SuperAdmin",
        },
        
        # 2️⃣ Admin
        {
            "email"             : "admin@test.com",
            "phone"             : "+8801500000002",
            "password"          : "123456ra",
            "first_name"        : "Mr.",
            "last_name"         : "Admin",
            "is_active"         : True,
            "is_superuser"      : False,
            "is_admin"          : True,
            "is_email_verified" : True,
            "is_phone_verified" : True,
            "group"             : "Admin",
        },

        # 3️⃣ Staff
        {
            "email"             : "staff@test.com",
            "phone"             : "+8801500000003",
            "password"          : "123456ra",
            "first_name"        : "Mr.",
            "last_name"         : "Staff",
            "is_active"         : True,
            "is_superuser"      : False,
            "is_admin"          : True,
            "is_email_verified" : True,
            "is_phone_verified" : True,
            "group"             : "Moderator",
        },

        # 4️⃣ Normal User
        {
            "email"             : "rakib1515hassan@gmail.com",
            "phone"             : "+8801500000004",
            "password"          : "123456ra",
            "first_name"        : "Mr.",
            "last_name"         : "Hassan",
            "is_active"         : True,
            "is_superuser"      : False,
            "is_admin"          : False,
            "is_email_verified" : True,
            "is_phone_verified" : True,
            "group"             : "Customer",
        }
    ]

    for data in users_data:
        group_name = data.pop("group")

        user, created = User.objects.get_or_create(
            email=data["email"],
            defaults=data
        )

        if created:
            user.set_password(data["password"])
            user.save()

        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except Group.DoesNotExist:
            pass
