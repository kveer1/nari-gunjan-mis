# test_mis.py
import os
import django
from django.test import TestCase

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ngmis.settings')
django.setup()

from students.models import Student, LearningCenter

class MISTestCase(TestCase):
    def setUp(self):
        self.center = LearningCenter.objects.create(
            name="Test Center",
            address="Test Address",
            village="Test Village",
            gram_panchayat="Test Panchayat",
            block="Test Block"
        )
        
    def test_student_creation(self):
        student = Student.objects.create(
            name="Test Student",
            date_of_enrollment="2023-01-01",
            mother_name="Test Mother",
            father_name="Test Father",
            gender="MALE",
            date_of_birth="2018-05-01",
            current_level=3,
            current_class=2,
            enrolled_in_govt_school=True,
            govt_school_class=2,
            center=self.center
        )
        
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(student.name, "Test Student")
        
    def test_center_creation(self):
        self.assertEqual(LearningCenter.objects.count(), 1)
        self.assertEqual(self.center.name, "Test Center")
        