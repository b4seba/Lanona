# pdf_generator.py

import os
import sys
import subprocess
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from tkinter import messagebox

def _open_pdf(filename):
    """Abre un archivo PDF dependiendo del sistema operativo."""
    try:
        if sys.platform.startswith('win'):
            os.startfile(filename)
        elif sys.platform.startswith('darwin'):
            subprocess.call(['open', filename])
        else:
            subprocess.call(['xdg-open', filename])
    except Exception:
        messagebox.showinfo("PDF Generado", f"Documento guardado como: {filename}")

def generar_pdf_documento(venta):
    filename = f"{venta['numero']}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter, topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Los Monitos de la Nona", styles['Title']))
    story.append(Paragraph(f"DOCUMENTO: {venta['tipo'].upper()}", styles['h2']))
    story.append(Spacer(1, 0.2*inch))

    info_data = [
        ['Número:', venta['numero']],
        ['Fecha:', datetime.fromisoformat(venta['fecha']).strftime('%d/%m/%Y %H:%M')],
        ['Vendedor:', venta['vendedor']]
    ]
    info_table = Table(info_data, colWidths=[1.2*inch, 2.5*inch])
    info_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))

    if venta['tipo'] == 'factura' and venta['cliente']:
        story.append(Paragraph("DATOS DEL CLIENTE", styles['h3']))
        cliente_data = [['Razón Social:', venta['cliente']['razon_social']], ['RUT:', venta['cliente']['rut']], ['Giro:', venta['cliente']['giro']], ['Dirección:', venta['cliente']['direccion']]]
        cliente_table = Table(cliente_data, colWidths=[1.2*inch, 4*inch])
        cliente_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'), ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold')]))
        story.append(cliente_table)
        story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("DETALLE", styles['h3']))
    
    headers = ['Cant.', 'Código', 'Producto', 'P. Unit.', 'Total']
    table_data = [headers]
    for item in venta['productos']:
        row = [item['cantidad'], item['codigo'], item['nombre'], f"${item['precio']:,.0f}", f"${item['total']:,.0f}"]
        table_data.append(row)

    products_table = Table(table_data, colWidths=[0.5*inch, 1*inch, 3*inch, 1*inch, 1*inch])
    products_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkslategray),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(products_table)
    story.append(Spacer(1, 0.3*inch))

    subtotal_text = f"Subtotal: ${venta['subtotal']:,.0f}"
    iva_text = f"IVA (19%): ${venta['iva']:,.0f}"
    total_text = f"TOTAL: ${venta['total']:,.0f}"

    if venta['tipo'] == 'factura':
        totales_data = [['', subtotal_text], ['', iva_text], ['', total_text]]
    else: # Boleta
        totales_data = [['', total_text]]

    totales_table = Table(totales_data, colWidths=[5*inch, 1.5*inch])
    totales_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('TEXTCOLOR', (-1,-1), (-1,-1), colors.red),
    ]))
    story.append(totales_table)
    
    doc.build(story)
    _open_pdf(filename)


def exportar_informe_pdf(fecha, vendedor, ventas):
    filename = f"Informe_Ventas_{fecha}_{vendedor}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Los Monitos de la Nona", styles['Title']))
    story.append(Paragraph(f"INFORME DE VENTAS - {fecha}", styles['h2']))
    if vendedor != "Todos":
        story.append(Paragraph(f"Vendedor: {vendedor}", styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    boletas = [v for v in ventas if v['tipo'] == 'boleta']
    facturas = [v for v in ventas if v['tipo'] == 'factura']

    if boletas:
        story.append(Paragraph("RESUMEN DE BOLETAS", styles['h3']))
        resumen_boletas = [
            ['Cantidad de boletas:', len(boletas)],
            ['Subtotal:', f"${sum(v['subtotal'] for v in boletas):,.0f}"],
            ['IVA (19%):', f"${sum(v['iva'] for v in boletas):,.0f}"],
            ['Total:', f"${sum(v['total'] for v in boletas):,.0f}"]
        ]
        table_boletas = Table(resumen_boletas)
        story.append(table_boletas)
        story.append(Spacer(1, 0.3 * inch))

    if facturas:
        story.append(Paragraph("DETALLE DE FACTURAS", styles['h3']))
        headers = ['Número', 'Cliente', 'Subtotal', 'IVA', 'Total']
        data = [headers]
        for f in facturas:
            cliente = f['cliente']['razon_social'] if f['cliente'] else 'N/A'
            data.append([f['numero'], cliente, f"${f['subtotal']:,.0f}", f"${f['iva']:,.0f}", f"${f['total']:,.0f}"])
        
        table_facturas = Table(data, colWidths=[1.5*inch, 2*inch, 1*inch, 1*inch, 1*inch])
        table_facturas.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkslategray),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        story.append(table_facturas)

    doc.build(story)
    _open_pdf(filename)