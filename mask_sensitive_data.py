import re
from docx import Document

input_file = "./data/影响大豆豆粕和豆油价格变动因素.docx"
output_file = "./data/masked_output.docx"

def mask_data(data, visible_start=3, visible_end=2, mask_char="*"):
    if len(data) <= visible_start + visible_end:
        return data  # too short to mask
    return data[:visible_start] + mask_char * (len(data) - visible_start - visible_end) + data[-visible_end:]

phone_regex = r'\b(\d{3})(\d{4})(\d{4})\b'  # match 11 digits phone number
id_regex = r'\b(\d{6})(\d{8})(\d{3})([0-9Xx])\b'  # match 18 personal ID number
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'  # match email address
address_regex = r'([\u4e00-\u9fa5]+[省市区县])[\u4e00-\u9fa5]+(路|街|村|镇|号|巷)[\u4e00-\u9fa5]*'  # match address(simple version)
bank_card_regex = r'\b\d{16,19}\b'  # match 16-19 digits bank card number(simple check)

doc = Document(input_file)
for paragraph in doc.paragraphs:
    text = paragraph.text

    text = re.sub(phone_regex, lambda m: mask_data(m.group(), visible_start=2, visible_end=2), text)
    text = re.sub(id_regex, lambda m: mask_data(m.group(), visible_start=2, visible_end=2), text)
    text = re.sub(email_regex, lambda m: m.group(0)[0] + "****@" + m.group(0).split('@')[1], text)
    text = re.sub(address_regex, lambda m: m.group(1) + "****", text)
    text = re.sub(bank_card_regex, lambda m: mask_data(m.group(), visible_start=2, visible_end=2), text)

    paragraph.text = text


doc.save(output_file)
print(f"masked data saved as '{output_file}'.")
