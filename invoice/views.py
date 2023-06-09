from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from .serializers import *
# Create your views here.


class RecordListAPI(generics.ListAPIView):

    authentication_classes = []
    serializer_class = RequestListSerializer
    queryset = Request.objects.all()

class PendingRecordListAPI(generics.ListAPIView):

    authentication_classes = []
    serializer_class = RequestListSerializer
    queryset = Request.objects.filter(status = "Pending")

class InvoiceSubmissionAPI(views.APIView):

    def post(self,request):

        data = request.data
        if 'UserId' not in data:
            return Response({"message":"UserId not provided"},status=status.HTTP_400_BAD_REQUEST)
        emp = Employee.objects.filter(id = data.pop("UserId"))
        if not emp.exists():
            return Response({"message":"User does not exist"},status=status.HTTP_400_BAD_REQUEST)
        submission_date = timezone.now().date()
        if 'Category' not in data:
            return Response({"message":"Category not provided"},status=status.HTTP_400_BAD_REQUEST)
        category = data.pop('Category')
        if 'InvoiceDate' not in data:
            return Response({"message":"InvoiceDate not provided"},status=status.HTTP_400_BAD_REQUEST)
        invoice_date = data.pop('InvoiceDate')
        if 'total_amount' not in data:
            return Response({"message":"total_amount not provided"},status=status.HTTP_400_BAD_REQUEST)
        total_amount = data.pop("total_amount")
        if 'way_of_payment' not in data:
            return Response({"message":"way_of_payment not provided"},status=status.HTTP_400_BAD_REQUEST)
        wop = data.pop('way_of_payment')
        try:
            with transaction.atomic():
                invoice = Invoice.objects.create(employee = emp.first(),date_of_invoice = invoice_date,category = category,total_amount=total_amount,way_of_payment = wop,**data)
                request = Request.objects.create(submission_date = submission_date,invoice=invoice)
                return Response({"message":"Request submission successful"},status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message":f"Could not create invoice because: {str(e)}"},status=status.HTTP_400_BAD_REQUEST)



class RequestStatusUpdateAPI(views.APIView):

    def post(self,request):

        data = request.data
        if 'request_id' not in data:
            return Response({"message":"request_id not provided"},status=status.HTTP_400_BAD_REQUEST)
        request = Request.objects.filter(id = data['request_id'])
        if not request.exists():
            return Response({"message":"Invalid Request Id provided"},status=status.HTTP_400_BAD_REQUEST)
        request = request.first()
        if 'status' not in data:
            return Response({"message":"status not provided"},status=status.HTTP_400_BAD_REQUEST)
        request.status = data['status']
        if 'remarks' in data:
            request.remarks = data['remarks']


        try:
            request.save()
            return Response({"message":f"Request status updated to {data['status']} successfully"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":f"Could not update request status because: {str(e)}"},status=status.HTTP_400_BAD_REQUEST)

