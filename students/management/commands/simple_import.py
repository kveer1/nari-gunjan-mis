import pandas as pd
from django.core.management.base import BaseCommand
from students.models import LearningCenter, Student
from datetime import datetime

class Command(BaseCommand):
    help = 'Simple import data from Excel file using position'

    def handle(self, *args, **options):
        try:
            file_path = 'Children Profile format_ LC of NG-One Centre.xlsx'
            self.stdout.write(self.style.SUCCESS(f'Simple import from {file_path}'))
            
            # Read Excel skipping the first 2 rows (header rows)
            df = pd.read_excel(file_path, sheet_name='Sheet1', header=2)
            self.stdout.write(self.style.SUCCESS(f'Found {len(df)} rows'))
            
            # Create center
            center, created = LearningCenter.objects.get_or_create(
                name="Basiyawan ASK",
                defaults={
                    'address': 'Village: Basiyawan, Gram Panchayat: Kalyanpur; Block: Punpun',
                    'village': 'Basiyawan',
                    'gram_panchayat': 'Kalyanpur',
                    'block': 'Punpun'
                }
            )
            
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Skip if name is empty (based on debug output, column 1 is serial number, column 2 is name)
                    if pd.isna(row.iloc[1]) or row.iloc[1] == '':
                        continue
                    
                    name = str(row.iloc[1]).strip()
                    self.stdout.write(f"Processing: {name}")
                    
                    # Map columns by position
                    # 0: Sl.No, 1: Name, 2: Enrollment Date, 3: Child ID, 4: Mother, 5: Father, 
                    # 6: Gender, 7: DOB, 8: Current Level, 9: Current Class, 10: Govt School, 11: Govt Class, 12: Remarks
                    
                    # Dates
                    enrollment_date = row.iloc[2] if not pd.isna(row.iloc[2]) else datetime.now().date()
                    if hasattr(enrollment_date, 'date'):
                        enrollment_date = enrollment_date.date()
                    
                    dob = row.iloc[7] if not pd.isna(row.iloc[7]) else datetime(2018, 1, 1).date()
                    if hasattr(dob, 'date'):
                        dob = dob.date()
                    
                    # Govt school
                    govt_school = str(row.iloc[10]).upper() in ['YES', 'Y', 'TRUE', '1'] if not pd.isna(row.iloc[10]) else False
                    govt_class = row.iloc[11] if not pd.isna(row.iloc[11]) else None
                    
                    # Create student
                    student = Student.objects.create(
                        name=name,
                        date_of_enrollment=enrollment_date,
                        date_of_birth=dob,
                        child_id=str(row.iloc[3]) if not pd.isna(row.iloc[3]) else '',
                        mother_name=str(row.iloc[4]) if not pd.isna(row.iloc[4]) else 'Unknown',
                        father_name=str(row.iloc[5]) if not pd.isna(row.iloc[5]) else 'Unknown',
                        gender='MALE' if str(row.iloc[6]).strip().upper() == 'MALE' else 'FEMALE',
                        current_level=int(row.iloc[8]) if not pd.isna(row.iloc[8]) else 1,
                        current_class=int(row.iloc[9]) if not pd.isna(row.iloc[9]) else 1,
                        enrolled_in_govt_school=govt_school,
                        govt_school_class=govt_class,
                        center=center,
                        remarks=str(row.iloc[12]) if not pd.isna(row.iloc[12]) else ''
                    )
                    
                    imported_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Imported: {name}'))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {index}: {e}"))
                    continue
            
            self.stdout.write(self.style.SUCCESS(f'Simple import completed: {imported_count} students imported'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            import traceback
            traceback.print_exc()
            