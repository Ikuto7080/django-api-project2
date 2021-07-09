from PIL import Image, ImageFont, ImageDraw
import uuid
import textwrap

# Image1 = Image.open('../staticfiles/share_image/kabegami.png')

# Image1copy =Image1.copy()

# Image2 = Image.open('../staticfiles/share_image/me.jpeg')

# Image2copy = Image2.copy()

# Image1copy.paste(Image2copy, (60, 80))

# my_image = Image.open(Image1copy)


# my_Image_file = Image1copy.save('../staticfiles/' + str(uuid.uuid4()) + '.png')

my_image = Image.open('../staticfiles/ee695d76-b9b7-4ea2-b313-1b8caf2d8911.png')

title_font = ImageFont.truetype('Avenir Next Condensed.ttc', 20)

title_text = "The Beauty of Nature"

image_editable = ImageDraw.Draw(my_image)

image_editable.text((8,8), title_text, (100, 100, 100), font=title_font)

my_image.save('../staticfiles/' + str(uuid.uuid4()) + '.png')

# image_editable.save('../staticfiles/' + str(uuid.uuid4()) + '.png')