import openai
import pkg_resources
import textwrap
from datetime import datetime
import requests
import json
from profanity_check import predict
from PIL import Image, ImageDraw, ImageFont
from pprint import pprint as pp


class OpenAIMaaS:

    def __init__(self, openai_api_key):
        openai.api_key = openai_api_key 

    def _get_image_prompt( self, day ):

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="give me a good random image prompt for a meme about it being {}. don't include text in the image. only the response. include something unusual.".format(day),
            max_tokens=1024,
        )

        text = response['choices'][0]['text'].strip()

        if(predict([text])):
            raise Exception('Bad prompt from: get_image_prompt')

        return text

    def _get_image_caption( self, day ):

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt="give me a good caption for a meme about it being {}.".format(day),
            max_tokens=1024
        )

        text = response['choices'][0]['text'].strip()
        
        if(predict([text])):
            raise Exception('Bad prompt from: get_image_caption')

        return text 

    def _get_image( self, prompt ):

        response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
        )
        image_url = response['data'][0]['url']

        # Download the image
        image_data = requests.get(image_url).content
        with open("image.jpg", "wb") as f:
            f.write(image_data)

    def _add_caption( self, caption ):

        # Open the image
        image = Image.open('image.jpg')

        # Create an ImageDraw object
        draw = ImageDraw.Draw(image)

        # Choose a font and font size
        #font = ImageFont.truetype('./fonts/impact.ttf', 72)
        font = ImageFont.truetype(pkg_resources.resource_filename("openai_maas", "fonts/impact.ttf"), 72)

        # Check the caption text so that it will fit on the image. Chunk it into lines if necessary 
        max_width = 30

        lines = textwrap.wrap(caption, width=max_width)

        bbox = font.getbbox('h')

        line_height = bbox[3] - bbox[1]

        total_height = line_height * len(lines)

        width, height = image.size

        # Calculate the x and y coordinates for the bottom center of the image
        x = 20 
        y = height - ( len(lines) * 75 ) - 15


        # Draw the text block
        for line in lines:
            text_width = draw.textlength(line, font=font)

            x = (width - text_width) // 2

            draw.text((x, y), line, font=font, align='center', stroke_width=3,stroke_fill='#000000')
            y += line_height + 15

        # Save the edited image
        image.save('edited_image.jpg')


    def dotw_meme( self, day=None ):

        if( day == None ):
            dt  = datetime.now()
            day = dt.strftime('%A') 

        prompt = self._get_image_prompt( day );

        self._get_image( prompt )

        caption = self._get_image_caption( day )

        print(caption)

        self._add_caption( caption )

        return {
            'prompt': prompt,
            'caption': caption
        }
