from pdfminer.high_level import extract_text
import PIL.Image
import tabula
import fitz
import io
                                                
# pdf_file takes a pdf_ object 
def converter(pdf_file, conv_type, pdf_file_path):
                                                
    if conv_type == 'text':
        text = extract_text(pdf_file)
        return text
                                                
    elif conv_type == 'table':
        tables = tabula.read_pdf(pdf_file, pages='all')
        return tables 
                                                
    elif conv_type == 'image':
        pdf_image_file = fitz.open(pdf_file_path)
        c = 1
                                                
        for i in range(len(pdf_image_file)):
            page = pdf_image_file[i]
            images = page.get_images()

            for j in images:
                raw_image = pdf_image_file.extract_image(j[0])
                data_image = raw_image["image"]
                image = PIL.Image.open(io.BytesIO(data_image))
                extension = raw_image['ext']
                image.save(open(f'data/img{c}.{extension}', 'wb'))
                image_file_name = f'img{c}.{extension}'
                c += 1
                                                
        return image_file_name

