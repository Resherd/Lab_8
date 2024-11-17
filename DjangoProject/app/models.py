from django.db import models

# Модель ліків
class Medicine(models.Model):
    registration_number = models.IntegerField(primary_key=True)  # Реєстраційний номер ліків
    name = models.CharField(max_length=100)  # Назва ліків
    manufacture_date = models.DateField()  # Дата виготовлення
    shelf_life_days = models.IntegerField()  # Термін зберігання в днях
    group_name = models.CharField(max_length=50)  # Група (Протизапальне, Знеболююче тощо)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Ціна ліків
    prescription_required = models.BooleanField()  # Відпускається за рецептом (Так/Ні)

    def __str__(self):
        return f'{self.name} - {self.price}'

# Модель постачальника
class Supplier(models.Model):
    supplier_code = models.IntegerField(primary_key=True)  # Код постачальника
    supplier_name = models.CharField(max_length=100)  # Назва постачальника
    address = models.CharField(max_length=255)  # Адреса постачальника
    phone = models.CharField(max_length=15)  # Телефон постачальника
    contact_person = models.CharField(max_length=100)  # Контактна особа
    location = models.CharField(max_length=50)  # Локація постачальника (Україна, інша країна)

    def __str__(self):
        return f'{self.supplier_name} - {self.phone}'

# Модель поставок
class Deliveries(models.Model):
    delivery_id = models.IntegerField(primary_key=True)  # Код поставки
    delivery_date = models.DateField()  # Дата поставки
    medicine_registration_number = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Реєстраційний номер ліків
    quantity = models.IntegerField()  # Кількість поставлених ліків
    supplier_code = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Код постачальника

    def __str__(self):
        return f'{self.medicine_registration_number.name} delivered by {self.supplier_code.supplier_name} on {self.delivery_date}'
