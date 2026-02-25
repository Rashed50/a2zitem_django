from django.contrib import admin

##? Models Import
from core.models.religion_model import Religion, ReligionDenomination
from core.models.file_model import RichTextEditorMediaFile
from core.models.address_model import Country, State, City

@admin.register(Religion)
class ReligionAdmin(admin.ModelAdmin):
    list_display        = ['id', 'name', 'slug']
    search_fields       = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ReligionDenomination)
class ReligionDenominationAdmin(admin.ModelAdmin):
    list_display        = ['id', 'name', 'slug', 'religion']
    search_fields       = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    
    
@admin.register(RichTextEditorMediaFile)
class RichTextEditorMediaFileAdmin(admin.ModelAdmin):
    list_display        = ['id', 'file', 'file_type', 'size', 'mime_type', 'original_name', 'checksum', 'object_id', 'content_type']
    search_fields       = ['file', 'file_type', 'size', 'mime_type', 'original_name', 'checksum', 'object_id', 'content_type']
    


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display        = ['id', 'name']
    search_fields       = ['id', 'name']
    # prepopulated_fields = {'slug': ('name',)}


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display        = ['id', 'name']
    search_fields       = ['id', 'name']
    # prepopulated_fields = {'slug': ('name',)}
    # autocomplete_fields = ['country']
    

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display        = ['id', 'name']
    search_fields       = ['id', 'name']
    # prepopulated_fields = {'slug': ('name',)}
    # autocomplete_fields = ['state']