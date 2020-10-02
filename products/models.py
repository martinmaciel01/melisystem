from django.db import models
from .utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse

#Custom queryset
class ProductQuerySet(models.query.QuerySet):
    
    def active(self):
        return self.filter(active = True)

    def featured(self):
        return self.filter(featured = True, active = True)

class ProductManager(models.Manager):
    
    def get_queryset(self):
        return ProductQuerySet(self.model, using = self._db)
    
    def all(self):
        return self.get_queryset().active()

    def featured(self):
        #self.get_queryset().filter(featured = True)
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id = id)
        if qs.count() == 1:
            return qs.first()
        return None

# Create your models here.

class Categoria(models.Model):
    cat_categoria = models.CharField(max_length=50, verbose_name='Categoria')
    def __str__(self):
        return self.cat_categoria    

class Sector(models.Model):
    sec_sector = models.CharField(max_length=50, verbose_name='Sector')
    sec_cat_id = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    def __str__(self):
        return self.sec_sector

class Grupo(models.Model):
    gru_grupo = models.CharField(max_length=50, verbose_name='Grupo')
    gr_sec_id = models.ForeignKey(Sector, on_delete=models.CASCADE)
    def __str__(self):
        return self.gru_grupo

class Product(models.Model): #product_category
    title       = models.CharField(max_length=20, verbose_name='Producto')
    slug        = models.SlugField(blank = True, unique = True)
    description = models.CharField(max_length=50, verbose_name='Descripción')
    text        = models.TextField(null=True, blank=True, verbose_name='Texto')
    categoria   = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    sector      = models.ForeignKey(Sector, on_delete=models.CASCADE)
    grupo       = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    prod_aroma  = models.CharField(max_length=50, null=True, blank=True, verbose_name='Aroma')
    prod_costo  = models.DecimalField(max_digits=5,decimal_places=2, default=0, verbose_name='CostoUn.')
    prod_markup = models.DecimalField(max_digits=5,decimal_places=2, default=0, verbose_name='%Markup')
    prod_stock  = models.DecimalField(max_digits=5,decimal_places=2, default=0, verbose_name='Stock')   
    image       = models.FileField(upload_to = 'products/', null = True, blank = True)
    featured    = models.BooleanField(default = False)
    active      = models.BooleanField(default = True)
    timestamp   = models.DateTimeField(auto_now_add = True)
    precio = models.DecimalField(max_digits=11,decimal_places=2, default=0, verbose_name='Precio Sugerido')
    def get_precio_sug(self):
        a = 1 + ( self.prod_markup / 100 )
        return self.prod_costo * a
    precio = property(get_precio_sug)

    objects = ProductManager()

    def get_absolute_url(self):
        #return "/products/{slug}/".format(slug = self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})
    
    #python 3
    def __str__(self):
        return self.title
        
    #python 2
    def __unicode__(self):
        return self.title

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender = Product)