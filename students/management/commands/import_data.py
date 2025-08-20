import pandas as pd
from django.core.management.base import BaseCommand
from students.models import LearningCenter, Student, Teacher, CommunityMobilizer
from datetime import datetime

class Command(BaseCommand):
    help = 'Import data from Excel file'

    def handle(self, *args, **options):
        try:
            file_path = 'Children Profile format_ LC of NG-One Centre.xlsx'
            self.stdout.write(self.style.SUCCESS(f'Importing data from {file_path}'))
            
            # Read the Excel file with proper header handling
            # First, let's read without header to see the actual structure
            df = pd.read_excel(file_path, sheet_name='Sheet1', header=None)
            self.stdout.write(self.style.SUCCESS(f'Raw Excel shape: {df.shape}'))
            
            # The actual data starts from row 3 (index 2) based on your file structure
            # Let's manually map the columns based on the debug output
            df = pd.read_excel(file_path, sheet_name='Sheet1', header=2)
            
            # Rename columns based on the debug output
            column_mapping = {
                1: 'sl_no',
                'NIRMAL KUMARI': 'name',
                datetime(2020, 1, 5, 0, 0): 'date_of_enrollment',
                'CH-214395': 'child_id',
                'URMILA DEVI': 'mother_name',
                'UPENDRA MANJHI': 'father_name',
                'FEMALE': 'gender',
                datetime(2016, 3, 5, 0, 0): 'date_of_birth',
                4: 'current_level',
                3: 'current_class',
                'YES': 'govt_school_enrolled',
                '3.1': 'govt_school_class',
                'Unnamed: 12': 'remarks'
            }
            
            df = df.rename(columns=column_mapping)
            self.stdout.write(self.style.SUCCESS(f'Columns after mapping: {list(df.columns)}'))
            
            # Create or get the learning center
            center, created = LearningCenter.objects.get_or_create(
                name="Basiyawan ASK",
                defaults={
                    'address': 'Village: Basiyawan, Gram Panchayat: Kalyanpur; Block: Punpun',
                    'village': 'Basiyawan',
                    'gram_panchayat': 'Kalyanpur',
                    'block': 'Punpun'
                }
            )
            
            # Import students
            imported_count = 0
            
            for index, row in df.iterrows():
                try:
                    # Skip empty rows
                    if pd.isna(row.get('name')) or row.get('name') == '':
                        continue
                    
                    self.stdout.write(f"Processing: {row.get('name')}")
                    
                    # Convert date strings to date objects
                    enrollment_date = row.get('date_of_enrollment')
                    if pd.isna(enrollment_date):
                        enrollment_date = datetime.now().date()
                    elif hasattr(enrollment_date, 'date'):
                        enrollment_date = enrollment_date.date()
                    
                    dob = row.get('date_of_birth')
                    if pd.isna(dob):
                        dob = datetime(2018, 1, 1).date()
                    elif hasattr(dob, 'date'):
                        dob = dob.date()
                    
                    # Handle govt school enrollment
                    govt_school_str = str(row.get('govt_school_enrolled', 'No')).upper()
                    govt_school = govt_school_str in ['YES', 'Y', 'TRUE', '1']
                    
                    govt_class = row.get('govt_school_class')
                    if pd.isna(govt_class) or govt_class in [0, '0']:
                        govt_class = None
                    
                    # Get other fields with defaults
                    child_id = row.get('child_id', '')
                    if pd.isna(child_id):
                        child_id = ''
                    
                    mother_name = row.get("mother_name", "Unknown")
                    if pd.isna(mother_name):
                        mother_name = "Unknown"
                    
                    father_name = row.get("father_name", "Unknown")
                    if pd.isna(father_name):
                        father_name = "Unknown"
                    
                    gender = row.get('gender', 'MALE')
                    if pd.isna(gender):
                        gender = 'MALE'
                    gender = 'MALE' if str(gender).strip().upper() == 'MALE' else 'FEMALE'
                    
                    current_level = row.get('current_level', 1)
                    if pd.isna(current_level):
                        current_level = 1
                    
                    current_class = row.get('current_class', 1)
                    if pd.isna(current_class):
                        current_class = 1
                    
                    remarks = row.get('remarks', '')
                    if pd.isna(remarks):
                        remarks = ''
                    
                    # Create student
                    student = Student.objects.create(
                        name=row['name'].strip(),
                        date_of_enrollment=enrollment_date,
                        date_of_birth=dob,
                        child_id=str(child_id),
                        mother_name=mother_name,
                        father_name=father_name,
                        gender=gender,
                        current_level=int(current_level),
                        current_class=int(current_class),
                        enrolled_in_govt_school=govt_school,
                        govt_school_class=govt_class,
                        center=center,
                        remarks=remarks
                    )
                    
                    imported_count += 1
                    self.stdout.write(self.style.SUCCESS(f'Imported: {row["name"]}'))
                        
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error importing row {index} ({row.get('name', 'Unknown')}): {e}"))
                    import traceback
                    traceback.print_exc()
                    continue
            
            self.stdout.write(self.style.SUCCESS(f'Import completed: {imported_count} students imported'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Excel file not found. Please make sure the file exists in the project root.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Unexpected error: {e}'))
            import traceback
            traceback.print_exc()