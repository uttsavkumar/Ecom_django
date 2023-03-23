from django.db import models
from django.conf import settings
# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    

class Product(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    discount_price = models.FloatField( blank=True)
    brand = models.CharField(max_length=200)


    def __str__(self):
        return self.name
    
ADDRESS_TYPE = (
    ('Home','Home'),
    ('Office','Office')
)

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=254,null=True)
    address = models.TextField()
    address_optional = models.TextField(null=True,blank=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)
    type = models.CharField(choices=ADDRESS_TYPE,null=True,max_length=50)

    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(default=1)


    def __str__(self):
        return self.item.name
    
    def getprice(self):
        return self.item.price * self.qty
    def getdiscountprice(self):
        return self.item.discount_price * self.qty
    def getdiscountpercentage(self):
        return round((self.item.price - self.item.discount_price) / self.item.price * 100)
    
    def getfinalamount(self):
        if self.item.discount_price:
            return self.getdiscountprice()
        else:
            return self.getprice()
        
class Coupon(models.Model):
    coupon = models.CharField(max_length=50)
    discount = models.FloatField()

    def __str__(self) :
        return self.coupon

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(blank=True,null=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True,blank=True)
    payment = models.OneToOneField("Payment", on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return self.user.username


    def totalamount(self):
        total = 0
        for orditem in self.items.all():
            total += orditem.getfinalamount()
        
        return total
    
    def deliveryfee(self):
        if self.totalamount() >= 5000:
            return 0
        else:
            return 150

    def coupondiscount(self):
        dis = 0
        if self.coupon:
            dis = self.coupon.discount
        return dis

    def totalpayableamount(self):
        return (self.totalamount() + self.deliveryfee()) - self.coupondiscount() 
    


class Payment(models.Model):
    TXNID = models.CharField(max_length=200)
    BANKTXNID = models.BigIntegerField()
    ORDERID = models.CharField(max_length=20, unique=True)
    TXNAMOUNT = models.FloatField()
    STATUS = models.CharField(max_length=50)
    TXNTYPE = models.CharField(max_length=20)
    PAYMENTMODE = models.CharField(max_length=200)
    REFUNDAMT = models.FloatField()
    TXNDATE = models.DateTimeField()

    def __str__(self):
        return self.ORDERID
