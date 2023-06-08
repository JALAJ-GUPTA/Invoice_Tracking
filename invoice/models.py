from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class Employee(models.Model):

    name = models.CharField(max_length=60,blank=True)
    email = models.EmailField( max_length=254,blank=True)
    lineManager = models.ForeignKey("Employee",related_name="subs",on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.name}"


invoice_choice = [
    ("Food","Food"),
    ("Travel","Travel"),
    ("Hotel","Hotel")
]

payment_choice =[
    ("UPI","UPI"),
    ("Cash","Cash"),
    ("Credit Card","Credit Card"),
    ("Debit Card","Debit Card")
]

class Invoice(models.Model):
    date_of_invoice = models.DateTimeField(null=True)
    category = models.CharField(max_length=20,choices=invoice_choice)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    employee = models.ForeignKey("Employee",related_name="invoices",on_delete=models.CASCADE)
    way_of_payment=models.CharField(max_length=50,choices=payment_choice)
    supplierGSTIN = models.CharField(max_length=50,blank=True)
    supplierUPI = models.CharField(max_length=50,blank=True)
    payeeACNO = models.CharField(max_length=50,blank=True)
    ifsc =  models.CharField(max_length=50,blank=True)
    invoiceNumber = models.CharField(max_length=50,blank=True)


    def __str__(self) -> str:
        return f"{self.employee.name} - {self.total_amount} - {self.date_of_invoice}"


request_choice = [
    ("Pending","Pending"),
    ("Rejected","Rejected"),
    ("Approved","Approved"),
    ("Hold","Hold")
]
class Request(models.Model):
    submission_date = models.DateTimeField(null=True)
    status=models.CharField(max_length=30,choices=request_choice,default="Pending")
    remarks=models.CharField(max_length=150,blank=True)
    invoice = models.OneToOneField("Invoice",related_name="request",on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.invoice.employee.name} - {self.submission_date} - {self.status}"
