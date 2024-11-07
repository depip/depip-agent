import html
from google.cloud import vision, translate_v2 
from PIL import Image, ImageDraw, ImageFont, ImageFile
from io import BytesIO
from typing import List
from google.cloud.vision_v1.types import BoundingPoly
class Data:
    bounds: List[BoundingPoly]
    original_text: str
    translate_client = None

    def __init__(self, bounds: List[BoundingPoly], original_text: str, target_language: str) -> None:
        self.bounds = bounds
        self.original_text = original_text

        if (self.translate_client == None):
            self.translate_client = translate_v2.Client()
            
        translate_text = self.translate_client.translate(self.original_text, target_language=target_language)
        self.translate_text = html.unescape(translate_text['translatedText'])

    def __repr__(self):
        return f"Data original: {self.original_text}; translated to: {self.translate_text}"

    def __str__(self):
        return f"Data original: {self.original_text}; translated to: {self.translate_text}"
class Manga:
    def __init__(self) -> None:
        self.vision_client = vision.ImageAnnotatorClient()

    def draw_boxes(self, image: ImageFile.ImageFile, datas: List[Data], color: str):
        draw = ImageDraw.Draw(image)
        for data in datas:
            polygon_points = [(data.bounds.vertices[0].x, data.bounds.vertices[0].y), 
                            (data.bounds.vertices[1].x, data.bounds.vertices[1].y), 
                            (data.bounds.vertices[2].x, data.bounds.vertices[2].y),
                            (data.bounds.vertices[3].x, data.bounds.vertices[3].y)
                            ]
            draw.polygon(
                polygon_points,
                "white",
                color,
            )
            x_coords, y_coords = zip(*polygon_points)
            min_x, min_y = min(x_coords), min(y_coords)
            max_x, max_y = max(x_coords), max(y_coords)
            polygon_width = max_x - min_x
            polygon_height = max_y - min_y
            
            def fits_text(text, font):
                bbox = draw.textbbox((0, 0), text, font=font)
                return bbox[2] - bbox[0] <= polygon_width and bbox[3] - bbox[1] <= polygon_height
            def split_text_to_lines(text, font, max_width):
                words = text.split()
                lines = []
                current_line = words[0]

                for word in words[1:]:
                    # Test if adding the next word would exceed the max width
                    test_line = current_line + ' ' + word
                    if draw.textbbox((0, 0), test_line, font=font)[2] - draw.textbbox((0, 0), test_line, font=font)[0] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)  # Add the last line
                return lines
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()
            lines = split_text_to_lines(text=data.translate_text,font=font, max_width=polygon_width)

            # Calculate total height for the text block (spacing between lines)
            total_text_height = sum(draw.textbbox((0, 0), line)[3] for line in lines)

            # Calculate starting Y position for centering the text vertically
            line_height = draw.textbbox((0, 0), lines[0], font=font)[3] - draw.textbbox((0, 0), lines[0], font=font)[1]
            start_y = min_y + (polygon_height - total_text_height) / 2

            # Draw each line of text inside the polygon
            for line in lines:
                text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
                start_x = min_x + (polygon_width - text_width) / 2  # Center the text horizontally
                draw.text((start_x, start_y), line, font=font, fill=(0, 0, 0))  # Draw the text line
                start_y += line_height + 2  # Move to the next line
        return image
    
    def get_document_bounds(self, image_file: bytes, destination_lang: str) -> List[Data]:
        blocks = []
        bounds = []
        datas = []

        image = vision.Image(content=image_file)
        
        response = self.vision_client.document_text_detection(image=image)
        document = response.full_text_annotation

        for page in document.pages:
            for block in page.blocks:
                block_text = ""
                for paragraph in block.paragraphs:
                    paragraph_text = " ".join("".join(symbol.text for symbol in word.symbols) for word in paragraph.words)
                    block_text += paragraph_text + " "

                blocks.append(block_text)
                bounds.append(block.bounding_box)
                
                data = Data(original_text=block_text, bounds=block.bounding_box, target_language=destination_lang)
                datas.append(data)
        return datas
    def render_doc_text(self, filein: bytes, destination_lang: str):
        # filein.seek(0)
        image = Image.open(BytesIO(filein))
        datas = self.get_document_bounds(filein, destination_lang)
        self.draw_boxes(image, datas, None)
        print( '\n'.join(str(data) for data in datas))

        return image
        # image.save('out.jpg')
        # if fileout != 0:
        #     image.save(fileout)
        # else:
        #     image.show()

    def translate_image(self, image: bytes, destination_lang: str):
        render_doc_response = self.render_doc_text(image, destination_lang)
        buffer = BytesIO()
        render_doc_response.save(buffer, render_doc_response.format)
        buffer.seek(0)
        return buffer