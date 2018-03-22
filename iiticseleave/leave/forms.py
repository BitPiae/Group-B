from django import forms
from django.contrib import admin
import leave.models

def log(f):
    def logged(*args, **kwargs):
        print(f, "called")
        ans = f(*args, **kwargs)
        print(f, "successfully returned")
        return ans
    return logged


class ApplicationChangeForm(forms.ModelForm):
    class Meta:
        model = leave.models.Application
        fields = ['applicant',
                  'typeOfLeave',
                  'startDate',
                  'endDate',
                  'prefix',
                  'suffix',
                  'reason',
                  'address',
                  'availLTC',
                  'submitted',
                  'recommended',
                  'recommender',
                  'recommender_comments',
                  'approved',
                  'approver',
                  'approver_comments']
    @log
    def clean(self):
        start_date = self.cleaned_data.get("startDate")
        end_date = self.cleaned_data.get("endDate")

        if end_date and start_date and end_date < start_date:
            msg = "End date should be greater than start date."
            self._errors["endDate"] = self.error_class([msg])
            raise forms.ValidationError(msg, code='invalid')


class ApplicationAdmin(admin.ModelAdmin):
    form = ApplicationChangeForm

    @log
    def get_readonly_fields(self, request, obj=None, **kwargs):
        applicant_cant_modify = ['applicant',
                                 'recommended',
                                 'recommender',
                                 'recommender_comments',
                                 'approved',
                                 'approver',
                                 'approver_comments']
        recommender_cant_modify = ['applicant',
                                  'typeOfLeave',
                                  'startDate',
                                  'endDate',
                                  'prefix',
                                  'suffix',
                                  'reason',
                                  'address',
                                  'availLTC',
                                  'submitted',
                                  'recommender',
                                  'approved',
                                  'approver',
                                  'approver_comments']
        approver_cant_modify = ['applicant',
                              'typeOfLeave',
                              'startDate',
                              'endDate',
                              'prefix',
                              'suffix',
                              'reason',
                              'address',
                              'availLTC',
                              'submitted',
                              'recommended',
                              'recommender',
                              'recommender_comments',
                              'approver',
                              ]
        supervisor_cant_modify =['applicant',
                              'typeOfLeave',
                              'startDate',
                              'endDate',
                              'prefix',
                              'suffix',
                              'reason',
                              'address',
                              'availLTC',
                              'submitted',
                              'recommended',
                              'recommender',
                              'recommender_comments',
                              'approved',
                              'approver',
                              'approver_comments']
        anything = ['applicant',
                  'typeOfLeave',
                  'startDate',
                  'endDate',
                  'prefix',
                  'suffix',
                  'reason',
                  'address',
                  'availLTC',
                  'submitted',
                  'recommended',
                  'recommender',
                  'recommender_comments',
                  'approved',
                  'approver',
                  'approver_comments']

        self.readonly_fields = [ ]
        if obj is not None:
            if obj.applicant == request.user:
                self.readonly_fields = applicant_cant_modify
                if obj.is_approved:
                    self.readonly_fields =  anything
            else:
                if request.user.is_admin:
                    self.readonly_fields = [ ]
                if request.user.is_supervisor:
                    self.readonly_fields = supervisor_cant_modify
                if request.user.is_recommender:
                    self.readonly_fields = recommender_cant_modify
                if request.user.is_approver:
                    self.readonly_fields = approver_cant_modify
        else:
            if request.user.is_supervisor:
                self.readonly_fields = supervisor_cant_modify
            if request.user.is_recommender:
                self.readonly_fields = recommender_cant_modify
            if request.user.is_approver:
                self.readonly_fields = approver_cant_modify
            if request.user.is_applicant:
                self.readonly_fields = applicant_cant_modify

        return self.readonly_fields

    @log
    def get_queryset(self, request):
        res = super(ApplicationAdmin, self).get_queryset(request)
        temp = res.filter(id=-1) # Empty result
        if request.user.is_admin:
            temp = res
        if request.user.is_supervisor:
            temp = res
        if request.user.is_recommender:
            temp = res.filter(submitted=True, recommender=request.user)
        if request.user.is_approver:
            temp = res.filter(recommended=True, submitted=True)
        if request.user.is_applicant:
            personal = res.filter(applicant=request.user)
            temp = temp | personal
        return temp


    @log
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'applicant':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)
        return super(ApplicationAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    @log
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'applicant', None) is None:
            obj.applicant = request.user
            obj.recommender = request.user.recommender
        if request.user.is_recommender:
            obj.recommender = request.user
        if request.user.is_approver:
            obj.approver = request.user
        obj.save()

    list_display = ('applicant',
                    'startDate',
                    'endDate',
                    'submitted',
                    'recommended',
                    'approved')

    @log
    def get_fieldsets(self, request, obj=None):
        if obj:
            if request.user == obj.applicant:
                return ((None, {'fields': (
                                            'typeOfLeave',
                                            'startDate',
                                            'endDate',
                                            'prefix',
                                            'suffix',
                                            'availLTC',
                                            'reason',
                                            'address'
                                            )}),
                        ('Status', {'fields': ('recommended',
                                                'recommender',
                                                'approved',
                                                'approver',
                                                'recommender_comments',
                                                'approver_comments')}),

                                        )
            else:
                if request.user.is_recommender:
                    return ((None, {'fields': ('applicant',
                                                'typeOfLeave',
                                                'startDate',
                                                'endDate',
                                                'prefix',
                                                'suffix',
                                                'availLTC',
                                                'reason',
                                                'address'
                                                )}),
                            ('Decision',{'fields':('recommender_comments',
                                                    'recommended',
                                                    )}),
                                            )
                if request.user.is_approver:
                    return ((None, {'fields': (
                                                'typeOfLeave',
                                                'startDate',
                                                'endDate',
                                                'prefix',
                                                'suffix',
                                                'availLTC',
                                                'reason',
                                                'address'
                                                )}),
                            ('Status', {'fields': ('recommender',
                                                    'recommender_comments',
                                                    )}),
                            ('Decision',{'fields':('approved','approver_comments')},))
        else:
            if request.user.is_admin:
                return ((None,{'fields': ('applicant',
                                        'typeOfLeave',
                                        'startDate',
                                        'endDate',
                                        'prefix',
                                        'suffix',
                                        'reason',
                                        'address',
                                        'availLTC',
                                        'submitted')}),)
            else:
                return ((None,{'fields': (
                                        'typeOfLeave',
                                        'startDate',
                                        'endDate',
                                        'prefix',
                                        'suffix',
                                        'reason',
                                        'address',
                                        'availLTC',
                                        'submitted')}),)

    list_filter = ('approved',
                   'recommended',
                   'submitted')

    search_fields = ('startDate',
                     'endDate',
                     'reason',
                     'submitted',
                     'recommended',
                     'approved')

    readonly_fields = []
    ordering = ('startDate', 'endDate')
    filter_horizontal = ()
