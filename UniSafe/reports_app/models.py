from django.db import models
from  users_app.models import *


class Report(models.Model):
    REPORT_FOR_CHOICES = [
        ('Self', 'Self'),
        ('Else', 'Else')
    ]
    
    report_id = models.CharField(primary_key=True,max_length=10, unique=True, editable=False, blank=False)
    created_on= models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending') # Pending, In Progress, Resolved, Rejected
    assigned_gd = models.ForeignKey(GenderDesk, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    # Reporter Contact Details
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='reported_cases')
    reporter_full_name = models.CharField(max_length=255, editable=False, blank=False)
    reporter_gender = models.CharField(max_length=6, blank= False)
    reporter_college = models.CharField(max_length=255, editable=False, blank=False)
    reporter_reg_no = models.CharField(max_length=255, editable=False)
    reporter_email = models.EmailField(editable=False, blank=False)
    reporter_phone = models.CharField(max_length=20, editable=False, blank=False)
    
    report_for = models.CharField(max_length=50, choices=REPORT_FOR_CHOICES)
    
    # # Victim's Details
    victim_email = models.EmailField()
    victim_full_name = models.CharField(max_length=255)
    victim_phone = models.CharField(max_length=20)
    victim_gender = models.CharField(max_length=6, blank= False)
    victim_reg_no = models.CharField(max_length=255)
    victim_college = models.CharField(max_length=255)
    
    # Description of the Abuse
    abuse_type = models.TextField(max_length=20, blank=False, null=False)
    date_and_time = models.DateTimeField()
    location = models.TextField(max_length=20, blank=False, null=False)
    description = models.TextField()
    evidence = models.FileField(upload_to='assets/evidence/', blank=True, null=True)
    
    # Perpetrator Details
    perpetrator_fullname = models.TextField(max_length=20, blank=False, null=False)
    perpetrator_gender = models.TextField(max_length=20, blank=False, null=False)
    relationship = models.TextField(max_length=20, blank=False, null=False)
    
    # Report Status
    police_status= models.CharField(max_length=20, default='Unfowarded')
    assigned_officer = models.ForeignKey(Police, on_delete=models.DO_NOTHING, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the instance is being created
            # Count all existing reports in the system
            total_reports = Report.objects.count() + 1
            self.report_id = f'RE-{self.reporter_reg_no}-{total_reports}'
        
            # profile = self.reporter.profile.student_profile
            # student = self.reporter
        
            # if self.report_for == 'Self':
            #     # Populate victim details from student's profile
            #     self.victim_email = student.email
            #     self.victim_full_name = student.full_name
            #     self.victim_phone = student.phone_number
            #     self.victim_gender = student.gender
            #     self.victim_college = profile.college
            #     self.victim_reg_no = profile.reg_no
        
        super().save(*args, **kwargs)