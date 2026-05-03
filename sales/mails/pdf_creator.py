import io
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from sales.models.models import Sale, SaleItem

# Türkçe karakter desteği için fontu tanımlıyoruz
# Docker içinde /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf yolunda yüklü olacak
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))

def generate_sale_receipt_pdf(sale_id):

    sale = Sale.objects.get(id=sale_id)
    items = sale.items.all()
    

    # Yerel saate çevir (İstanbul GMT+3)
    local_time = timezone.localtime(sale.created_at)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles ve Font ayarı
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    title_style.fontName = 'DejaVuSans'
    
    normal_style = styles['Normal']
    normal_style.fontName = 'DejaVuSans'

    elements.append(Paragraph(f"ECZANE SATIŞ FİŞİ", title_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Fiş No: {sale.id}", normal_style))
    elements.append(Paragraph(f"Tarih: {local_time.strftime('%d.%m.%Y %H:%M')}", normal_style))
    elements.append(Spacer(1, 12))

    data = [["İlaç Adı", "Adet", "Birim Fiyat", "Toplam"]]
    for item in items:
        data.append([
            item.medicine.name,
            str(item.quantity),
            f"{item.price} TL",
            f"{item.quantity * item.price} TL"
        ])
    data.append(["", "", "GENEL TOPLAM:", f"{sale.total_amount} TL"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans'), # Tabloya fontu uygula
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer
