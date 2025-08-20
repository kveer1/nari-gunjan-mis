# scripts/import_data.py
import os
import django
import pandas as pd
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngmis.settings')
django.setup()

from students.models import LearningCenter, Student, Teacher, CommunityMobilizer

def import_from_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path, sheet_name='Sheet1', header=2)
    
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
    
    # Create teacher
    teacher, created = Teacher.objects.get_or_create(
        name="Nikita Kumari",
        defaults={
            'center': center,
            'date_of_joining': datetime(2025, 3, 7).date(),
            'contact_number': '6299366636'
        }
    )
    
    # Create CM
    cm, created = CommunityMobilizer.objects.get_or_create(
        name="Sunil Kumari",
        defaults={
            'date_of_joining': datetime(2022, 6, 22).date()
        }
    )
    
    # Import students
    for index, row in df.iterrows():
        if pd.notna(row['Name of the child']):
            # Convert date strings to date objects
            try:
                enrollment_date = row['Date of Enrollment at Nari Gunjan L.C.']
                if isinstance(enrollment_date, str):
                    enrollment_date = datetime.strptime(enrollment_date, '%Y-%m-%d %H:%M:%S').date()
                elif hasattr(enrollment_date, 'date'):
                    enrollment_date = enrollment_date.date()
                    
                dob = row['Date of Birth (DD/MM/YYYY)']
                if isinstance(dob, str):
                    dob = datetime.strptime(dob, '%Y-%m-%d %H:%M:%S').date()
                elif hasattr(dob, 'date'):
                    dob = dob.date()
                    
                # Handle govt school enrollment
                govt_school = str(row['Whether the child is enrolled in govt School or not (Yes/ No)']).upper() == 'YES'
                govt_class = row['If yes, then in which class']
                if pd.isna(govt_class) or govt_class == 0:
                    govt_class = None
                    
                Student.objects.create(
                    name=row['Name of the child'],
                    date_of_enrollment=enrollment_date,
                    child_id=row['Child ID'] if pd.notna(row['Child ID']) else '',
                    mother_name=row["Mother's name"],
                    father_name=row["Father's name"],
                    gender=row['Sex (Male / Female)'],
                    date_of_birth=dob,
                    current_level=row['Current Level at the Learning Centre'],
                    current_class=row['Current class at the Coming Centre'],
                    enrolled_in_govt_school=govt_school,
                    govt_school_class=govt_class,
                    center=center,
                    remarks=row['Remarks'] if pd.notna(row['Remarks']) else ''
                )
            except Exception as e:
                print(f"Error importing row {index}: {e}")
                continue

if __name__ == "__main__":
    import_from_excel('Children Profile format_ LC of NG-One Centre.xlsx')
    print("Data import completed!")