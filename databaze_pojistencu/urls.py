from django.urls import path, include
from . import views
from . import url_handlers

urlpatterns = [	
    path("pojistenec_index/", views.PojistenecIndex.as_view(), name="pojistenec_index"),
    path("<int:pk>/pojistenec_detail/", views.CurrentPojistenecView.as_view(), name="pojistenec_detail"),
    path("vytvorit_pojistenec/", views.VytvoritPojistenec.as_view(), name="novy_pojistenec"),	
    path("<int:pk>/edit/", views.EditPojistenec.as_view(), name="edit_pojistenec"),
    path("register/", views.UzivatelViewRegister.as_view(), name = "registrace"),
    path("login/", views.UzivatelViewLogin.as_view(), name = "login"),
    path("logout/", views.logout_user, name = "logout"),
    path("", url_handlers.index_handler),
]
