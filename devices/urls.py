from django.urls import path
from .views import EnrollDevice, ApproveDevice, BlockDevice, HeartbeatView, ManifestView

urlpatterns = [
    path("devices/enroll/", EnrollDevice.as_view(), name="devices-enroll"),
    path("devices/<int:device_id>/approve/", ApproveDevice.as_view(), name="devices-approve"),
    path("devices/<int:device_id>/block/", BlockDevice.as_view(), name="devices-block"),
    path("devices/<int:device_id>/heartbeat/", HeartbeatView.as_view(), name="devices-heartbeat"),
    path("devices/<int:device_id>/manifest/", ManifestView.as_view(), name="devices-manifest"),
]
