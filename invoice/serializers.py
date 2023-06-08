from rest_framework import serializers

from .models import *

class InvoiceSerializer(serializers.ModelSerializer):


    class Meta:
        model = Invoice
        fields = ('date_of_invoice','category','total_amount','supplierGSTIN','way_of_payment','supplierUPI','payeeACNO','ifsc','invoiceNumber')


class RequestListSerializer(serializers.ModelSerializer):

    invoice = InvoiceSerializer()
    class Meta:
        model = Request
        fields = ('invoice','id','submission_date','status')

