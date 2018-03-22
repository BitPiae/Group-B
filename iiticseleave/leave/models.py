from django.db import models

class Application(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    address = models.TextField()
    applicant = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True)
    choices = (
        ('EL', 'Earned Leave'),
        ('HPL', 'Half Pay Leave'),
        ('OT', 'Other Leave'),
        )
    type_of_leave = models.CharField(choices=choices,max_length=3, default='OT')
    prefix = models.PositiveIntegerField(default=0, help_text="In days")
    suffix = models.PositiveIntegerField(default=0, help_text="In days")
    avail_ltc = models.BooleanField(default=False)

    submitted = models.BooleanField(default=False)
    recommended = models.BooleanField(default=False)
    recommender = models.ForeignKey('accounts.User',on_delete=models.CASCADE, blank=True, null=True, related_name="Recommender")
    recommender_comments = models.TextField(blank=True, null=True)

    approved = models.BooleanField(default=False)
    approver = models.ForeignKey('accounts.User',on_delete=models.CASCADE, blank=True, null=True, related_name="Approver")
    approver_comments = models.TextField(blank=True, null=True)

    def __str__(self):
         return str(self.applicant.get_full_name()) + " from " + str(self.start_date) + " - " + str(self.end_date)

    @property
    def is_submitted(self):
        return self.submitted

    @property
    def full_name(self):
        return self.applicant.get_full_name()

    @property
    def is_recommended(self):
        return self.recommended

    @property
    def is_approved(self):
        return self.approved
