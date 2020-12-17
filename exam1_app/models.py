from django.db import models
import re
import bcrypt

# Create your models here.

class userManager(models.Manager):
    def regValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        errors = {}
        if len(postData['f_name']) < 2:
            errors['fnamereq'] = 'First name should be more than 2 characters!'
        if len(postData['l_name']) < 2:
            errors['lnamereq'] = 'Last name should be more than 2 characters!'
        if len(postData['email']) == 0:
            errors['emailreq'] = 'Email is required!'
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        else:
            repeatEmail = User.objects.filter(email = postData['email'])
            if len(repeatEmail) > 0:
                errors['emailTaken'] = "This email is taken!"
        if len(postData['pw']) < 8:
            errors['pwreq'] = 'Password must be at least 8 characters!'
        if postData['pw'] != postData['pw2']:
            errors['nomatch'] = 'Passwords should match!'
        return errors


    def loginValidator(self, postData):
        errors = {}
        usersWithEmail = User.objects.filter(email=postData['email'])
        if len(postData['email']) == 0:
            errors['userEmailReq'] = "Email is required"
        elif len(usersWithEmail) == 0:
            errors['userEmailWrong'] = "Email is not registered"
        else:
            user = usersWithEmail[0]
            if bcrypt.checkpw(postData['pw'].encode(), usersWithEmail[0].password.encode()):
                print('Passwords Match')
            else: 
                errors['wrongPw'] = "Incorrect Password"
        return errors

class ItemManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['item']) < 3:
            errors["item"] = "Item name must be at least 3 characters."
        if len(postData['desc']) < 3:
            errors["desc"] = "description must be at least 3 characters."
        return errors


class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    wisher = models.ForeignKey(User, related_name = 'made_wish', on_delete=models.CASCADE)
    date_granted = models.DateTimeField(null = True)
    likes = models.ManyToManyField(User, related_name='liked')
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
