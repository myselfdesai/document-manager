from django.conf import settings
from rest_framework.routers import DefaultRouter

from propylon_document_manager.file_versions.api.views import FileUploadViewSet, FileVersionsViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = DefaultRouter()

router.register("file_upload", FileUploadViewSet, basename="fileupload")
router.register("file_versions", FileVersionsViewSet, basename="fileversions")

app_name = "api"
urlpatterns = router.urls
