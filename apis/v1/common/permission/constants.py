ALLOWED_PERMISSION_MODELS = {
    "auth"     : ["group", "permission"],
    "users"    : ["user"],
    "employee" : ["employee"],
    "company"  : ["company", "department", "designation", "subscriptionplan"],
}


"""
!Note:- Permission system = lowercase(ModelClassName)
🧠 Django rule (সবচেয়ে গুরুত্বপূর্ণ)

Django permission এই ২টা জিনিস দিয়ে তৈরি হয়:

1️⃣ app_label → app এর নাম
2️⃣ model → model class নামের lowercase

📌 File কোথায় আছে (models.py, models/events.py) সেটা matter করে না
📌 Matter করে শুধু app config
"""