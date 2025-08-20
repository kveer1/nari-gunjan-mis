import pandas as pd
from django.core.management.base import BaseCommand
from students.models import LearningCenter, Student, Teacher, CommunityMobilizer
from datetime import datetime

class Command(BaseCommand):
    help = 'Debug import data from Excel file'

    def handle(self, *args, **options):
        try:
            file_path = 'Children Profile format_ LC of NG-One Centre.xlsx'
            self.stdout.write(self.style.SUCCESS(f'Debugging data import from {file_path}'))
            
            # Read the Excel file
            df = pd.read_excel(file_path, sheet_name='Sheet1', header=2)
            self.stdout.write(self.style.SUCCESS(f'Excel file shape: {df.shape}'))
            
            # Show column names
            self.stdout.write(self.style.SUCCESS(f'Columns: {list(df.columns)}'))
            
            # Show first few rows
            self.stdout.write(self.style.SUCCESS('First 5 rows:'))
            for i, row in df.head().iterrows():
                self.stdout.write(f"Row {i}: {dict(row)}")
            
            # Check if file exists and has data
            center, created = LearningCenter.objects.get_or_create(
                name="Basiyawan ASK",
                defaults={
                    'address': 'Village: Basiyawan, Gram Panchayat: Kalyanpur; Block: Punpun',
                    'village': 'Basiyawan',
                    'gram_panchayat': 'Kalyanpur',
                    'block': 'Punpun'
                }
            )
            
            # Test student creation
            test_student, created = Student.objects.get_or_create(
                name="TEST STUDENT",
                date_of_birth=datetime(2018, 1, 1).date(),
                defaults={
                    'date_of_enrollment': datetime(2023, 1, 1).date(),
                    'mother_name': 'Test Mother',
                    'father_name': 'Test Father',
                    'gender': 'MALE',
                    'current_level': 1,
                    'current_class': 1,
                    'enrolled_in_govt_school': False,
                    'center': center,
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS('Test student created successfully'))
            else:
                self.stdout.write(self.style.WARNING('Test student already exists'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback
            traceback.print_exc()
            