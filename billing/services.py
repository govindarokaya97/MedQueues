from .models import Bill, BillItem
from laboratory.models import LabRequest
from pharmacy.models import Prescription


def generate_bill(appointment):

    # Prevent duplicate bill
    if hasattr(appointment, "bill"):
        return appointment.bill

    bill = Bill.objects.create(
        patient=appointment.patient,
        appointment=appointment,
        discount=0,
        tax=0,
        payment_method="Cash",
        payment_status="Pending",
    )

    # -------------------------
    # Doctor Consultation Fee
    # -------------------------

    doctor_fee = appointment.doctor.consultation_fee

    BillItem.objects.create(
        bill=bill,
        service_name="Doctor Consultation",
        quantity=1,
        unit_price=doctor_fee
    )

    # -------------------------
    # Laboratory Charges
    # -------------------------

    lab_request = LabRequest.objects.filter(
        appointment=appointment
    ).first()

    if lab_request:

        for item in lab_request.items.select_related(
            "lab_test"
        ):

            BillItem.objects.create(
                bill=bill,
                service_name=item.lab_test.name,
                quantity=1,
                unit_price=item.lab_test.price
            )

    # -------------------------
    # Pharmacy Charges
    # -------------------------

    prescription = Prescription.objects.filter(
        appointment=appointment
    ).first()

    if prescription:

        for item in prescription.items.select_related(
            "medicine"
        ):

            BillItem.objects.create(
                bill=bill,
                service_name=item.medicine.name,
                quantity=item.quantity,
                unit_price=item.medicine.price
            )

    # After creating all BillItems
    bill.amount = bill.subtotal
    bill.total_amount = bill.grand_total
    bill.save()

    return bill

