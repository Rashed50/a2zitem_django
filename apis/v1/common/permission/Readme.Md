# Permission system = lowercase(ModelClassName)
🧠 Django rule (সবচেয়ে গুরুত্বপূর্ণ)

## Django permission এই ২টা জিনিস দিয়ে তৈরি হয়:

1. app_label → app এর নাম
2. model → model class নামের lowercase

📌 File কোথায় আছে (models.py, models/events.py) সেটা matter করে না
📌 Matter করে শুধু app config

## তোমার models → app_label + model name

✅ users\models.py
```bash
class User(AbstractBaseUser, TimestampedModel, PermissionsMixin):
    ...
```
🔹 app_label → users
🔹 model name → user (class নাম lowercase)

👉 Permissions হবে:
```bash
add_user
change_user
delete_user
view_user
```

✅ apps\events\models\events.py
```bash
class Event(TimestampedModel):
    ...
```

🔹 app_label → events
🔹 model name → event

👉 Permissions:
```bash
add_event
change_event
delete_event
view_event
```

Case–1️⃣: Model class নাম যদি UserProfile
```bash
class UserProfile(models.Model):
    ...
```
কী লিখবে?
```bash
"users": ["userprofile"]
```
🔹 Rule:
- Class name → UserProfile
- Permission model name → userprofile (lowercase, no underscore)

👉 Permissions হবে:
```bash
add_userprofile
change_userprofile
delete_userprofile
view_userprofile
```

## তাহলে তোমার ALLOWED_PERMISSION_MODELS কী হবে?
```bash
ALLOWED_PERMISSION_MODELS = {
    "users": ["user"],
    "events": ["event", "announcement"],
}
```

## 100% নিশ্চিত হতে চাইলে (Live check)
Shell এ চালাও 👇
```bash
python manage.py shell
```
```bash
from django.contrib.contenttypes.models import ContentType

ContentType.objects.filter(app_label="events").values("app_label", "model")
```
Output আসবে:
[
    {'app_label': 'events', 'model': 'event'},
    {'app_label': 'events', 'model': 'announcement'},
]
