from config.env import env

STORAGES = {
    "default": {  # 👉 media only
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key"  : env("AWS_ACCESS_KEY_ID"),
            "secret_key"  : env("AWS_SECRET_ACCESS_KEY"),
            "bucket_name" : env("AWS_STORAGE_BUCKET_NAME"),
            "region_name" : env("AWS_S3_REGION_NAME"),

            # "location"       : "media",
            "file_overwrite" : False,
            "default_acl"    : None,

            "custom_domain": f"{env('AWS_STORAGE_BUCKET_NAME')}.s3.amazonaws.com",
        },
    },
    
    "staticfiles": {  # ❗ REQUIRED even if you don't use S3 for static
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}