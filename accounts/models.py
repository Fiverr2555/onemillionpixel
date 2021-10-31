from django.db import models

# Create your models here.

class userBlock(models.Model):
    address = models.CharField(max_length=200)
    blocks = models.IntegerField(default=0)


class Block(models.Model):
    useraddress = models.ForeignKey(userBlock,default=None,on_delete=models.CASCADE,null=True, blank=True)
    image = models.ImageField(upload_to='img/blocks/',default=0)
    SX = models.IntegerField(default=40)
    SY = models.IntegerField(default=40)
    EX = models.IntegerField(default=40)
    EY = models.IntegerField(default=40)
    block_no = models.IntegerField(default=0)
    no_of_blocks = models.IntegerField(default=1)
    block_text = models.CharField(max_length=140, default='e')
    twitter = models.TextField(default=None,null=True,blank=True)
    discord = models.TextField(default=None,null=True,blank=True)
    instagram = models.TextField(default=None,null=True,blank=True)
    telegram = models.TextField(default=None,null=True,blank=True)
    website = models.TextField(default=None,null=True,blank=True)
    status = models.BooleanField(default=False)