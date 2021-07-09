from PIL import Image 

Image1 = Image.open('../staticfiles/share_image/east_asia.jpeg')

Image1copy =Image1.copy()

Image2 = Image.open('../staticfiles/share_image/shopee.png')

Image2copy = Image2.copy()

Image1copy.paste(Image2copy, (0, 0))

Image1copy.save('../staticfiles/pasted2.png')