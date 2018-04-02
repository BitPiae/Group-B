- [ ] Added a recommender field in Accounts model
- [ ] Added recommender in fieldset accounts forms.py
- [ ] Changed on_delete in application to cascade so Admin can delete users.
- [ ] removed __init__ in  ApplicationAdmin(admin.ModelAdmin) not doing anything
- [ ] Changed start_date end_date error to correct place
- [ ] removed list(set()) from leave get_readonly_fields
- [ ] removed from account add form 'classes': ('wide',),
- [ ] removed : password = ReadOnlyPasswordHashField() from UserChangeForm(forms.ModelForm).


- [ ] MAJOR BUG: Applicant is able to change everything if he goes to edit form.

- [ ] Major Bug 
- [ ] TODO: Add upcoming functionality
- [ ] TODO: Make PhD Accounts
- [X] TODO: Remove view site button top right

- [ ] TODO: Make printing better
- [ ] TODO: Figure out how to make typeOfLeave, startDate, endDate, render beautifully.
- [ ] TODO: Figure out how prevent PhD students from deleting forms
- [ ] TODO: Supervisor can modify settings of other user.

 22nd march
- [ ] TODO: Print form ke liye template.
- [ ] TODO: Admin can't change user's password.
- [ ] TODO: make recommender compulsory if user is applicant
- [X] TODO: Add custom save buttons
- [X] TODO: Set server time equal IST.
- [X] TODO: Make sure prefix and suffix are non-negative
- [X] TODO: If application is approved or recommended then delete is allowed
- [ ] TODO: Customize logout message

# TODO
- [X] Admin
    - [X] User
      - [X] edit
      - [X] add
      - [X] remove
    - [X] application
      - [X] add
      - [X] view
      - [X] edit
    - [X] password reset
- recommender
- approver
- applicant
  - [X] User

  - [ ] appliations

- Supervisor

- [ ] made text style consistent, added hints,
