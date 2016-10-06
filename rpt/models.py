from django.db import models
from thumbs import ImageWithThumbsField

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    age = models.IntegerField()
    address = models.CharField(max_length=255,blank=True,null=True)
    image = ImageWithThumbsField(upload_to='static/%Y/%m/%d', sizes=((90,
                                 120), (128, 128), (160, 160), (240, 240)),
                                 blank=True, null=True)

    def __unicode__(self):
        return self.name
