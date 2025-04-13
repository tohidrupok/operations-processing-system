from django.db import models

#Abstract Base
class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='media/logos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

# Company, Supplier, MenPower all inherit Organization
class Company(Organization):
    pass

class Supplier(Organization):
    pass

class MenPower(Organization):
    pass

#Item Category 
class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#Item Model
class Item(models.Model):
    item_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='media/item_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item_name

#Project Model
class Project(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    approximate_bill = models.DecimalField(max_digits=12, decimal_places=2)
    current_cost = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    final_bill = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    current_paid = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.company.name})"


#Memo for item purchases
class Memo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='item_memos')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='memos')
    items = models.ManyToManyField(Item, related_name='memos')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Memo - {self.project.name}"


# Memo for manpower payment
class ManpowerMemo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='manpower_memos')
    worker = models.ForeignKey(MenPower, on_delete=models.CASCADE, related_name='memos')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Manpower Memo - {self.project.name}"
