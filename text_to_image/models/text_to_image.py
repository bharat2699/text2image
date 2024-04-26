from django.db import models
import uuid


class TextToImage(models.Model):
    id = models.AutoField(primary_key=True)
    prompt = models.TextField(null=True, blank=True)
    sd_api_request = models.JSONField(null=True, blank=True)
    sd_api_response = models.JSONField(null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        default="pending",
        choices=[
            ("pending", "pending"),
            ("completed", "completed"),
            ("failed", "failed"),
        ],
    )
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    exception = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Text To Image"
        verbose_name_plural = "Text To Images"

    def __str__(self):
        return self.str(uuid)
