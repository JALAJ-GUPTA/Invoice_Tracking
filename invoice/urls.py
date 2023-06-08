from django.urls import path
from .views import *

urlpatterns = [
    path('record_list',RecordListAPI.as_view() ),
    path('pending_record_list',PendingRecordListAPI.as_view() ),
    path('invoice_submission',InvoiceSubmissionAPI.as_view() ),
]