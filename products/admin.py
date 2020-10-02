from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.db.models.signals import post_save
from .models import Product
from .models import Categoria
from .models import Sector
from .models import Grupo

class ProductAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'grupo', 'prod_costo', 'prod_markup', 'precio')
	class meta:
		model = Product
	search_fields 	= ('title', 'description', 'grupo')
	list_filter = ('sector', 'grupo')
	list_per_page = 20
	list_editable = ('prod_markup',)

class ListandoSector(admin.ModelAdmin):
	list_display = ('sec_sector', 'sec_cat_id')

class ListandoGrupo(admin.ModelAdmin):
	list_display = ('gru_grupo', 'gr_sec_id')

admin.site.register(Product, ProductAdmin)
admin.site.register(Categoria)
admin.site.register(Sector, ListandoSector)
admin.site.register(Grupo, ListandoGrupo)
