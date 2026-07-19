from .models import Bill, BillItem
from laboratory.models import LabRequest
from pharmacy.models import Prescription
from django.db import transaction


@transaction.atomic
def generate_bill(appointment):

    bill, created= Bill.objects.get_or_create(
        appointment = appointment,
        defaults={
            "patient": appointment.patient,
        }
    )
    
    if not created:
        return bill
    # -------------------------
    # Doctor Consultation Fee
    # -------------------------
    
    BillItem.objects.create(
        bill=bill,
        service_name="Doctor Consultation",
        service_type="Consultation",
        quantity=1,
        unit_price=appointment.doctor.consultation_fee,
    )

    # -------------------------
    # Laboratory Charges
    # -------------------------

    lab_requests = LabRequest.objects.filter(
        appointment=appointment
    )

    for request in lab_requests:
        
        for item in request.items.all():

            BillItem.objects.create(
                bill=bill,
                service_name=item.lab_test.name,
                service_type="Laboratory",
                quantity=1,
                unit_price=item.lab_test.price
            )

    # -------------------------
    # Pharmacy Charges
    # -------------------------
    try:
        prescription = appointment.prescription

        for item in prescription.items.all():

            BillItem.objects.create(
                bill=bill,
                service_name=item.medicine.name,
                service_type="Medicine",
                quantity=item.quantity,
                unit_price=item.medicine.price
            )
    
    except Prescription.DoesNotExist:
        pass

    bill.amount = bill.subtotal
    bill.total_amount = bill.grand_total
    bill.save(update_fields=["amount","total_amount"])

    return bill

