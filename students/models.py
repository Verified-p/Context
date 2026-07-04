from django.db import models
from django.conf import settings


class Student(models.Model):

    TRAINING_MODE = (
        ('PHYSICAL', 'Physical'),
        ('ONLINE', 'Online'),
        ('HYBRID', 'Hybrid'),
    )

    SESSION = (
        ('MORNING', 'Morning'),
        ('EVENING', 'Evening'),
        ('WEEKEND', 'Weekend'),
    )

    STATUS = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Completed'),
    )

    GENDER_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    # ==================================
    # PERSONAL INFORMATION
    # ==================================

    full_name = models.CharField(
        max_length=255
    )

    admission_number = models.CharField(
        max_length=100,
        unique=True
    )

    national_id = models.CharField(
        max_length=20,
        unique=True
    )

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True
    )

    phone_number = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    county = models.CharField(
        max_length=100,
        blank=True
    )

    sub_county = models.CharField(
        max_length=100,
        blank=True
    )

    physical_address = models.TextField(
        blank=True
    )

    # ==================================
    # INSTITUTION DETAILS
    # ==================================

    institution = models.CharField(
        max_length=255
    )

    department = models.CharField(
        max_length=255,
        blank=True
    )

    course = models.CharField(
        max_length=255
    )

    specialization = models.CharField(
        max_length=255,
        blank=True
    )

    year_of_study = models.CharField(
        max_length=50,
        blank=True
    )

    duration = models.CharField(
        max_length=50
    )

    start_date = models.DateField()

    end_date = models.DateField()

    training_mode = models.CharField(
        max_length=20,
        choices=TRAINING_MODE
    )

    session = models.CharField(
        max_length=20,
        choices=SESSION
    )

    # ==================================
    # ATTACHMENT / INTERNSHIP DETAILS
    # ==================================

    attachment_company = models.CharField(
        max_length=255,
        blank=True
    )

    attachment_supervisor = models.CharField(
        max_length=255,
        blank=True
    )

    supervisor_phone = models.CharField(
        max_length=20,
        blank=True
    )

    supervisor_email = models.EmailField(
        blank=True
    )

    # ==================================
    # EMERGENCY CONTACT
    # ==================================

    emergency_contact_name = models.CharField(
        max_length=255,
        blank=True
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True
    )

    emergency_relationship = models.CharField(
        max_length=100,
        blank=True
    )

    # ==================================
    # DOCUMENTS
    # ==================================

    passport_photo = models.ImageField(
        upload_to='students/passports/'
    )

    id_copy = models.ImageField(
        upload_to='students/ids/'
    )

    introduction_letter = models.FileField(
        upload_to='students/letters/'
    )

    # ==================================
    # APPROVAL DETAILS
    # ==================================

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='PENDING'
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_students'
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # ==================================
    # SYSTEM DETAILS
    # ==================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.full_name

    @property
    def is_approved(self):
        return self.status == "APPROVED"

    @property
    def training_period(self):
        return f"{self.start_date} - {self.end_date}"