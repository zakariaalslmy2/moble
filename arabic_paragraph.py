from PIL import ImageFont, ImageDraw, Image
from arabic_reshaper import reshape
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors





class ArabicParagraph:
    def __init__(self):
        self.punctuation = [".", ",", "?", "!", ":", ";", "\"", "'", "/", "(", ")", "[", "]", ".", "-", "—", "<", ">", "%", "$", "*", "^", "="]

    def reshaper_text(self, text):
        return get_display(reshape(text))

    def clean_text(self, text):
        # تنظيف النص من الأسطر الفارغة الزائدة
        lines = [line.strip() for line in text.split('\n')]
        return '\n'.join(line for line in lines if line)

    def ArabicParagraph(self, text, font_name, path, col_width, font_size, align="RIGHT"):
        pdfmetrics.registerFont(TTFont(font_name, path))
        
        # تنظيف النص وتقسيمه إلى أسطر
        text = self.clean_text(text)
        lines = text.split('\n')
        
        table_data = []
        for line in lines:
            if not line.strip():
                table_data.append([''])  # إضافة سطر فارغ
                continue
                
            reshaped_line = self.reshaper_text(line.strip())
            current_line = ''
            words = reshaped_line.split()
            
            for word in words:
                test_line = f"{current_line} {word}".strip()
                # استخدام ImageFont لحساب عرض النص
                font = ImageFont.truetype(path, font_size)
                line_width = font.getlength(test_line)
                
                if line_width > col_width:
                    if current_line:
                        table_data.append([current_line])
                    current_line = word
                else:
                    current_line = test_line
                    
            if current_line:
                table_data.append([current_line])

        # إنشاء الجدول مع التنسيق
        table = Table(table_data, colWidths=[col_width], hAlign=align)
        table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, -1), font_size),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),  # إضافة مساحة بين الأسطر
        ]))

        return table