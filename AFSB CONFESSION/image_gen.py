from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import random

def create_confession_image(confession_text, output_path):
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Create random greyscale gradient background
    gradient = Image.new("RGB", (width, height))
    for y in range(height):
        shade = int(255 * (y / height))
        for x in range(width):
            gradient.putpixel((x, y), (shade, shade, shade))
    image.paste(gradient)

    # Draw white rounded rectangle for the card
    margin = 60
    card = Image.new("RGB", (width - 2*margin, height - 2*margin), "white")
    mask = Image.new("L", card.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([0, 0, *card.size], radius=80, fill=255)
    image.paste(card, (margin, margin), mask)

    draw = ImageDraw.Draw(image)

    # Load a large system font (change size here!)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
        header_font = ImageFont.truetype("arialbd.ttf", 60)
    except:
        font = ImageFont.load_default()
        header_font = font

    # Header
    header_text = "afsbconfession"
    header_w, header_h = draw.textbbox((0, 0), header_text, font=header_font)[2:]
    draw.text(((width - header_w) / 2, 120), header_text, fill="deeppink", font=header_font)

    # Wrap the confession
    wrapper = textwrap.TextWrapper(width=35)
    wrapped = wrapper.fill(text=confession_text)

    # Calculate position to center confession
    confession_w, confession_h = draw.multiline_textbbox((0, 0), wrapped, font=font)[2:]
    confession_x = (width - confession_w) / 2
    confession_y = (height - confession_h) / 2 + 40

    draw.multiline_text((confession_x, confession_y), wrapped, font=font, fill="black", align="center")

    image.save(output_path)
