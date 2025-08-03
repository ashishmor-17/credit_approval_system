from django.core.management.base import BaseCommand
from credit_approval.tasks import ingest_customer_data, ingest_loan_data


# to ingrst data from Excel files into the database using Celery tasks
class Command(BaseCommand):
    help = "Ingests customer_data.xlsx and loan_data.xlsx into the database using Celery tasks."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Ingesting customer data..."))
        ingest_customer_data.delay()
        self.stdout.write(self.style.WARNING("Ingesting loan data..."))
        ingest_loan_data.delay()
        self.stdout.write(self.style.SUCCESS("Data ingestion tasks have been dispatched to Celery."))
