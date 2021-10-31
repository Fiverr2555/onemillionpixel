from os import X_OK
from django.db import models
from django.shortcuts import redirect, render
from .models import Block,userBlock
from PIL import Image
from django.http import JsonResponse
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# Create your views here.

from background_task import background
from django.contrib.auth.models import User

@background(schedule=900)
def notify_user():
    # lookup user by id and send them a message
    print("updating addresses")
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Creds0.json',scope) # get email and key from creds
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key("1PddsYWXx5TfaFWIgt2reDQ2yUwdPvQtmoDmsUSVH8wk").worksheet("Block Owners")
    df = pd.DataFrame.from_dict(sheet.get_all_values())
    df.columns = ['address','no_of_blocks']
    for address,blocks in zip(df['address'],df['no_of_blocks']):
        try:
            user_block = userBlock.objects.get(address=address)
            user_block.blocks = blocks
        except(userBlock.DoesNotExist):
            user_block = userBlock(
            address = address,
            blocks = blocks
        )
        user_block.save()
    print("checking for non authorized addresses")
    user_blocks = userBlock.objects.all()
    for user_block in user_blocks:
        print(user_block.address)
        auth = False
        for address in df['address']:
            if user_block.address == address:
                print('authorized')
                auth = True
                break
            else:
                auth = False
        if auth == False:
            print('non authorized block found')
            user_block.delete

    print("addresses updated")
    

def home(request):
    #notify_user()
    blocks = Block.objects.all().order_by('id')
    context={
        'blocks': blocks
    }
    return render(request,'index.html',context)

def addImageView(request):
    
    if request.user.username != 'admin':
        return redirect('/')
    context={}
    if request.GET.get('request_block'):
        block = Block.objects.get(id=request.GET.get('request_block'))
        context={
            'request_block':block
        }
    if request.method == 'POST':
        option = request.POST.get('option')
        print(option)
        if request.POST.get('request_block'):
            block = Block.objects.get(id=request.POST.get('request_block'))
            img = Image.open(block.image)
        else:
            img = Image.open(request.FILES['image'])
        
        block_no =  request.POST.get('block_no')
        block_no = int(block_no)
          
        block_row = block_no//25
        if block_no%25 == 0:
           block_row = block_row - 1 

        if (block_no > 25):
            x = 40*(block_no-(block_row*25 + 1))
        else:
            x = 40*(block_no - 1)
        
        
        background = Image.open('media/img/out.png')
        y = block_row * 40
        offset = x,y
        ratio1 = int(request.POST.get('ratio1'))*40
        ratio2 = int(request.POST.get('ratio2'))*40
        count_block = int(request.POST.get('ratio1'))*int(request.POST.get('ratio2'))
        img = img.resize((ratio1, ratio2))
        background.paste(img, offset)
        
        background.save('media/img/out.png')
        print(ratio1)
        print(x)
        print(x + 40*count_block)
        print(request.POST.get('block_no'))
        if option == 'upload':
            if request.POST.get('request_block'):
                block.SX = x
                block.SY = y
                block.EX = x + ratio1
                block.EY = y + ratio2
                block.no_of_blocks = count_block
                block.status = True
                block.block_no = request.POST.get('block_no')
            else:
                block = Block(
                    SX = x,
                    SY = y,
                    EX = x + ratio1,
                    EY = y + ratio2,
                    no_of_blocks = count_block,
                    status = True,
                    block_no = request.POST.get('block_no')
                )
            block.save()
        else:
            block = Block.objects.get(block_no=request.POST.get('block_no'))
            block.delete

            
    
    return render(request,'addimage.html',context)

def addAddressView(request):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('Creds0.json',scope) # get email and key from creds
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key("1PddsYWXx5TfaFWIgt2reDQ2yUwdPvQtmoDmsUSVH8wk").worksheet("Block Owners")
    df = pd.DataFrame.from_dict(sheet.get_all_values())
    df.columns = ['address','no_of_blocks']
    for address,blocks in zip(df['address'],df['no_of_blocks']):
        try:
            user_block = userBlock.objects.get(address=address)
            user_block.blocks = blocks
        except(userBlock.DoesNotExist):
            user_block = userBlock(
            address = address,
            blocks = blocks
        )
        user_block.save()
    print("checking for non authorized addresses")
    user_blocks = userBlock.objects.all()
    for user_block in user_blocks:
        print(user_block.address)
        auth = False
        for address in df['address']:
            if user_block.address == address:
                print('authorized')
                auth = True
                break
            else:
                auth = False
        if auth == False:
            print('non authorized block found')
            user_block.delete
    return JsonResponse({'message':'addresses updated'})

def userFormView(request):
    error = False
    address = request.GET.get('address')
    message = ''
    try:
        userblock = userBlock.objects.all()
        for b in userblock:
            if b.address.lower() == address:
                error = False
                no_of_blocks = b.blocks
                break
            else:
                error = True
        if error == True:
            return redirect('/'+'?error=true')
        
    except(userBlock.DoesNotExist):
        return redirect('/'+'?error=true')

    if request.method == 'POST':
        print(address)
        userblock = userBlock.objects.all()
        for b in userblock:
            print(b.address)
            if b.address.lower() == address:
                print('test')
                error = False
                no_of_blocks = b.blocks
                address = b.address
                break
            else:
                error = True
        if error == True:
            return redirect('/'+'?error=true')
        user_address = userBlock.objects.get(address=address)
        block = Block(
            useraddress = user_address,
            image = request.FILES['image'],
            no_of_blocks = no_of_blocks,
            block_text = request.POST.get('text'),
            twitter = request.POST.get('twitter'),
            website = request.POST.get('website'),
            instagram = request.POST.get('instagram'),
            discord = request.POST.get('discord'),
            telegram = request.POST.get('telegram'),
        )
        block.save()
        message = 'request submitted successfully!'
    return render(request,'userForm.html',{'no_of_blocks':no_of_blocks,'message':message})

def requestView(request):
    if request.user.username != 'admin':
        return redirect('/')
    request_blocks = Block.objects.filter(status=False)
    context={
        'request_blocks':request_blocks
    }
    return render(request,'requests.html',context)

def faqView(request):
    return render(request,'faq.html',{})