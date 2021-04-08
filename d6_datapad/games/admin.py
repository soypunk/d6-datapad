from django.contrib import admin

from .models import Game

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_by', 'created')
    list_filter = ("created_by",)
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def get_changeform_initial_data(self, request):
        get_data = super(GameAdmin, self).get_changeform_initial_data(request)
        get_data['created_by'] = request.user.pk
        return get_data    

admin.site.register(Game,GameAdmin) 
