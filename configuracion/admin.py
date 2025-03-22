from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from configuracion.models import variablesModels
from tipocortina.models import Tipocaida, Tipomando, Tiptubo

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(Group)
class GroupAdmin(ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    change_password_form = AdminPasswordChangeForm
    form = UserChangeForm


class ReadOnlyBaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    ordering = ('name',)


@admin.register(Tipocaida)
class TipocaidaAdmin(ReadOnlyBaseAdmin):
    pass


@admin.register(Tipomando)
class TipomandoAdmin(ReadOnlyBaseAdmin):
    pass


@admin.register(Tiptubo)
class TiptuboAdmin(ReadOnlyBaseAdmin):
    pass


@admin.register(variablesModels)
class VariablesConfigAdmin(ModelAdmin):
    pass
