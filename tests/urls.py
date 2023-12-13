from django.urls import include, path

from umsebenzi.urls import router

urlpatterns = [
    path('umsebenzi/', include(router.urls)),
]