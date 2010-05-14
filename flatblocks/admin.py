from django.contrib import admin
from flatblocks.models import FlatBlock, BlockSet, BlockSetItem
 
class FlatBlockAdmin(admin.ModelAdmin):
    ordering = ['slug',]
    list_display = ('slug', 'header', 'content')
    search_fields = ('slug', 'header', 'content')

class FlatBlockSetInline(admin.TabularInline):
    model = BlockSetItem
    extra = 1

class BlockSetAdmin(admin.ModelAdmin):
    inlines = [FlatBlockSetInline,]

admin.site.register(FlatBlock, FlatBlockAdmin)
admin.site.register(BlockSet, BlockSetAdmin)
