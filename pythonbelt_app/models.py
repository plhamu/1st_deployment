from django.db import models
from datetime import date
import re

class UserManager(models.Manager):
    def registerValidator(self, postData):
        errors= {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # ClassName.objects.exclude(field1="value for field1", etc)-gets any records matching the query provided
        matchingEmail= User.objects.filter(email= postData['e'])
        print(f"users with matching email: {matchingEmail}")
        if len(postData['fname']) == 0:
            errors['fname_req']= "First Name is required!"
        elif len(postData['fname'])<3:
           errors['fname_length']= "First Name should be 3 characters!"
        if len(postData['lname']) == 0:
            errors['lname_req']= "Last Name is required!"
        elif len(postData['lname'])<3:
            errors['lname_length']= "Last Name should be 3 characters!"
        if len(postData['e'])== 0:
            errors['email_req']="Email is Required!"
        elif not EMAIL_REGEX.match(postData['e']):# test whether a field matches the pattern            
            errors['invalid_email'] = "Invalid email address!"
        if len(matchingEmail)>0:
            errors['email_taken']='Email is taken!'
        if len(postData['pw'])== 0:
            errors['pw_req']="Password is Required!"
        elif len(postData['pw'])< 8:
            errors['pwlength']="Password should be 8 characters!"
        if postData['pw']!= postData['cpw']:
            errors['match']= "Password should match!"
        return errors
        
    def loginValidator(self, postData):
        errors ={}
        matchingEmail = User.objects.filter(email= postData['e'])
        if len(matchingEmail)==0:
            errors['emailNotFound']="Email is not registered!"
        else: 
            print(matchingEmail[0].password)
            if matchingEmail[0].password != postData['pw']:
                errors['pwIncorrect']='Password is Incorrect!'
        return errors

class TripManager(models.Manager):
    def createTripValidator(self, postData):
        errors={}
        today= str(date.today())
        if len(postData['dest'])== 0:
            errors['dest_req']="No Empty Entries"
        if postData['date_from'] <= today:
            errors['start_date']= "Start Date should be in Future!"
        if postData['date_to'] < today:
            errors['end_date']= "End Date should be in Future!"
        return errors
# Create your models here.
class User(models.Model):
    first_name =models.CharField(max_length=255)
    last_name =models.CharField(max_length=255)
    email =models.CharField(max_length=255)
    password =models.CharField(max_length=255)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects= UserManager()
    
    def __str__(self):
        return f"<User objects: {self.first_name} {self.id}"

class Trip(models.Model):
    name= models.CharField(max_length=255)
    start_date=models.DateField()
    end_date=models.DateField()
    plan= models.TextField()
    creator=models.ForeignKey(User, related_name="trips_created", on_delete=models.CASCADE)
    travelor=models.ManyToManyField(User, related_name="trips_traveled")
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)
    objects=TripManager()

    def __str__(self):
        return f"<Trip objects: {self.name} {self.id}"