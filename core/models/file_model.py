import os, hashlib, mimetypes
from PIL import Image

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

##? Utils Import
from core.models.time_stamped import TimestampedModel2

class RichTextEditorMediaFile(TimestampedModel2):

    class FileType(models.TextChoices):
        IMAGE = "image", "Image"
        FILE  = "file",  "File"

    file = models.FileField(
        verbose_name = _("Media File"),
        upload_to    = "richtext/",
    )

    file_type = models.CharField(
        verbose_name = _("File Type"),
        max_length   = 10,
        choices      = FileType.choices,
        editable     = False
    )

    size = models.PositiveIntegerField(
        verbose_name = _("File Size (bytes)"),
        editable     = False,
        null         = True
    )

    mime_type = models.CharField(
        verbose_name = _("Mime Type"),
        max_length = 100,
        editable   = False
    )

    original_name = models.CharField(
        verbose_name = _("Original Name"),
        max_length = 255,
        editable   = False
    )
    
    checksum = models.CharField(
        verbose_name = _("Checksum"),
        max_length = 64,
        editable   = False,
        unique     = True,
        db_index   = True,
        null       = True
    )

    ##! Generic relation fields
    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Content Type"))
    object_id      = models.PositiveIntegerField(null=True, blank=True, verbose_name=_("Object ID"))
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self): 
        return f"{self.file.name} - {self.file_type} - {self.size} bytes"
    
    class Meta:
        # Prevent duplicate per context
        unique_together = ("checksum", "content_type", "object_id")

    def clean(self):
        if not self.file:
            raise ValidationError("File is required")
        
        # Extension validation
        ext = os.path.splitext(self.file.name)[1].lower()
        allowed_ext = [".jpg", ".jpeg", ".png", ".webp", ".pdf", ".docx"]
        if ext not in allowed_ext:
            raise ValidationError("Invalid file extension")

        # Size validation (5MB)
        max_size = 5 * 1024 * 1024
        if self.file.size > max_size:
            raise ValidationError("File size must be under 5MB")

        # Mime type validation
        mime_type = (
            self.file.content_type
            if hasattr(self.file, "content_type") and self.file.content_type
            else mimetypes.guess_type(self.file.name)[0]
        )

        allowed_mime_types = [
            "image/jpeg", "image/png", "image/webp",
            "application/pdf",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ]

        if mime_type not in allowed_mime_types:
            raise ValidationError("Unsupported file type")
        
    def save(self, *args, **kwargs):
        # Run validation
        self.full_clean()

        file = self.file

        # File size & original name
        self.size = file.size
        self.original_name = file.name

        # Mime type
        if hasattr(file, "content_type") and file.content_type:
            self.mime_type = file.content_type
        else:
            self.mime_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"

        # File type detection
        if self.mime_type.startswith("image"):
            self.file_type = self.FileType.IMAGE
        else:
            self.file_type = self.FileType.FILE

        ## Checksum [checksum is a unique fingerprint of the file]
        # file.seek(0)
        # checksum = hashlib.sha256(file.read()).hexdigest()
        # file.seek(0)

        # Duplicate check: যদি checksum আগেই থাকে, তাহলে শুধু return
        # Check if file with same checksum + context exists
        # existing = RichTextEditorMediaFile.objects.filter(
        #     checksum     = checksum,
        #     content_type = self.content_type,
        #     object_id    = self.object_id
        # ).first()

        # if existing:
        #     # Update current instance with existing ID (avoid duplicate save)
        #     self.id = existing.id
        #     self.checksum = existing.checksum
        #     super().save(update_fields=[])  # avoid modifying other fields
        # else:
        #     self.checksum = checksum
        super().save(*args, **kwargs)

    
