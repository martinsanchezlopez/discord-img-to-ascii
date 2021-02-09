from PIL import Image, ImageStat, ImageFont, ImageDraw
import sys
import discord
import os
import requests

YOUR_TOKEN = '' #discord bot token

MAX_B = 255 #max brightness


PIXEL_X_SIDE = 10 # I have no clue what this does anymore tbh 



charactersAll = ".'`,^:;~-_+i!lI?\|()1]*&%$#@"
characters = ".':~+?]*&$#@@"




def convertImage(url, imgFormat, darkMode='1'):
    
    img = Image.open(requests.get(url, stream=True).raw).convert('L')
    
    size = img.size
    

    char = characters#All
    
    
    if darkMode=='0':
        char = char[::-1]
        
    brightnessStops = len(char)

    charList = []
    firstPass = True
    charXLength = 0

    xSide = PIXEL_X_SIDE #int(size[0]/resolution) #x pixel size
    ySide = int( (PIXEL_X_SIDE*size[1])/size[0])       #int(size[1]/resolution) #y pixel size
    
    
    for j in range (0, size[1]-ySide, xSide):
        for i in range (0 , size[0]-xSide, ySide):
            region = img.crop( (i, j, (i+xSide), (j+ySide)) )
            #medianList.append(ImageStat.Stat(region).median)
            
            regionBrightness = ImageStat.Stat(region).median[0]/MAX_B
            if regionBrightness != 0:
                charList.append(char[int(brightnessStops*(regionBrightness)-1)])
            else:
                charList.append(char[0])
        
        if firstPass:
            charXLength = len(charList)
            firstPass = False
        charList.append("L")
        
    if imgFormat == "jpeg":
        if darkMode:
            color = 0
        else:
            color = 255
        
        #print(len(charList), charXLength)
        #newSize = (int( (10*(size[0]-xSide))/ySide ), int( ((size[1]-ySide))/ySide ))
        mult= 6.85
        
        newSize = (int(charXLength*mult), int(1.85*mult* (len(charList)/charXLength) ) )
        
        
        output = Image.new('RGB', newSize,color = (54, 57, 63) )
        font = ImageFont.truetype("courier.ttf", 10)
        draw = ImageDraw.Draw(output)
        #draw.ellipse([150, 150, 500, 500], 'red')
        fontFill = (255,255,255,255)
        draw.text((0,0), imageString(charList), font=font, fill='white')
        return output
        #output.show()
        #output.save('ascii_img.jpeg', "JPEG")
    elif imgFormat == "txt":
        writeTxt(charList)
    else:
        print("wrong format")
    
def imageString(charList):
    lineP=''
    for i in charList:
        if i != 'L':
            lineP += i
        else:
            lineP+= "\n"
    return lineP
    


def writeTxt(charList):
    str= imageString(charList)

    txtFile = open('./ascii_img.txt','w')
    txtFile.write(str)

    txtFile.close()



client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!txtfy'):
        imgId = message.reference.message_id
        responseMsg = await message.channel.fetch_message(imgId)
        URL = responseMsg.attachments[0].url
        

        convertImage(URL, 'jpeg').save("response.jpg")
        await message.channel.send(file=discord.File('response.jpg'))

client.run(YOUR_TOKEN)


