from django.db import models
import uuid
from authentication.models import User

VENDOR_CATEGORY = [
    ('food', 'Foods'),
    ('cake_pastries', 'Cakes and Pastries'),
    ('shar_pizza_grillz', 'Sharwarma, Pizza and Grillz'),
    ('snacks', 'Snacks and Small Chops'),
    ('others', 'Others'),
]

FOOD_CATEGORY = [
    ('rice', 'RICE'),
    ('cake_pastries', 'Cakes and Pastries'),
    ('swallow', 'Swallow'),
    ('proteins', 'Proteins'),
    ('soft_drinks', 'Soft Drinks'),
    ('juice', 'Juice'),
    ('yogourt', 'Yogourt'),
    # ('gtillz', 'Soft Drinks'),
]


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-name']


class VendorInformation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=225, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    password = models.CharField(max_length=10, blank=True)
    email = models.EmailField()
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE)
    # opening_time = models.TimeField()
    # closing_time = models.TimeField()
    file = models.FileField(upload_to='vendor_profile', blank=True)
    address = models.CharField(max_length=250, blank=True)
    category = models.ManyToManyField(Category, )
    delivery_time = models.CharField(max_length=250, blank=False)

    opening_time = models.TimeField()
    closing_time = models.TimeField()

    profile_updated = models.BooleanField(default=False, )

    sub_account_code = models.CharField(max_length=50)

    successful_order_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} {self.id}"

    class Meta:
        verbose_name_plural = 'VendorInformation'
        ordering = ("-successful_order_count", "name")

    def update_vendor_profile(self, validated_data):
        self.file = validated_data['file']
        print("Validated Data going to model => ", validated_data)
        self.address = validated_data['address']
        self.category = validated_data['category']
        self.profile_updated = True

        self.save()
        return ("Vendor Profile Updated Successfully")

    def update_vendor_subaccount(self, sub_account_code):
        self.sub_account_code = sub_account_code
        self.save()
        return ("Sub Account Created Successfully")

    def update_order_count(self):
        self.successful_order_count += 1
        self.save()


class MenuItems(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(VendorInformation,
                               on_delete=models.CASCADE,
                               blank=True,
                               default=None)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(choices=FOOD_CATEGORY,
                                max_length=100,
                                blank=True)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.id}"

    class Meta:
        verbose_name_plural = 'MenuItems'
