import streamlit as st

import pandas as pd

from pathlib import Path
from io import BytesIO, StringIO

from reportlab.pdfgen.canvas import Canvas

from reportlab.lib.pagesizes import letter

from reportlab.platypus import Table

from reportlab.lib import colors
import imageio.v3 as iio

from PIL import Image

from imageio import mimwrite

import io

import csv

import tempfile

def string_to_array(string):
    return string.split(',')

def create_pdf(company_name, company_logo, seller_website ,seller_name, seller_ruc, client_name, date, concept, csv_data):
    if company_name is None or seller_name is None or seller_ruc is None or client_name is None or date is None or concept is None:
        st.error("Por favor, ingrese todos los datos")
        return

    c = Canvas("factura.pdf", pagesize=letter)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, 750, str(company_name).upper())

    # derecha
    c.setFont('Helvetica', 12)
    c.drawString(400, 670, "FECHA:      " + str(date))
    c.setFont('Helvetica-Bold', 12)
    c.drawString(400, 650, str(seller_website))


    # imagen
    if company_logo is not None:
        image = Image.open(company_logo)
        temp_image_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_image_path = temp_image_file.name
        image.save(temp_image_path)
        temp_image_file.close()
        c.drawImage(temp_image_path, 400, 680, width=100, height=100)

    # izquierda

    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, 730, "FACTURA: ")
    c.drawString(100, 700, "DE")
    c.setFont('Helvetica', 12)
    c.drawString(100, 680, str(seller_name).upper())
    c.drawString(100, 660, seller_ruc)

    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, 630, "FACTURADO A")
    c.setFont('Helvetica', 12)
    c.drawString(100, 610, client_name)
    c.drawString(100, 590, "Concepto:     " + concept)

    stringio = StringIO(csv_data.getvalue().decode("utf-8"))
    data = stringio.read()

    columns = string_to_array(data.split('\n')[0])
    data = data.split('\n')[1:]

    for i in range(len(columns)):
        c.setFont('Helvetica-Bold', 12)
        c.drawString(100 + i * 180, 550, columns[i])

    c.setFont('Helvetica', 12)
    for i in range(len(data)):
        row = string_to_array(data[i])
        for j in range(len(row)):
            c.drawString(100 + j * 180, 530 - i * 20, row[j])

    c.setFont('Helvetica-Bold', 12)

    total_sum = 0

    for i in range(len(data)):
        row = string_to_array(data[i])
        for j in range(len(row)):
            if j % 2 != 0:
                total_sum += float(row[j])


    c.drawString(100, 550 - 30 - len(data) * 20 , "Total: " )
    c.drawString(100 + 180, 550 - 30 - len(data) * 20, str(total_sum))


    c.save()

    st.success("Factura generada correctamente")

def main():
    st.set_page_config(page_title="Generador de facturas",
                       page_icon=":pencil")

    if("company_name" not in st.session_state):
        st.session_state.company_name = None

    if("seller_name" not in st.session_state):
        st.session_state.seller_name = None

    if("seller_website" not in st.session_state):
        st.session_state.seller_website = None

    if("seller_ruc" not in st.session_state):
        st.session_state.seller_ruc = None

    if("client_name" not in st.session_state):
        st.session_state.client_name = None

    if("date" not in st.session_state):
        st.session_state.date = None

    if("concept" not in st.session_state):
        st.session_state.concept = None

    if("company_logo" not in st.session_state):
        st.session_state.company_logo = None

    st.header('Programa de generar facturas')

    upload_file = st.file_uploader('Ingresar  archivo CSV o Excel con el detalle de la factura', type=['csv', 'xlsx'])

    if upload_file is not None:
        if st.button('Generar factura'):
            with st.spinner('Generando factura...'):
                create_pdf(st.session_state.company_name, st.session_state.company_logo, st.session_state.seller_website ,st.session_state.seller_name, st.session_state.seller_ruc, st.session_state.client_name, st.session_state.date, st.session_state.concept, upload_file)


    if "company_logo" in st.session_state and st.session_state.company_logo is not None:
        st.image(st.session_state.company_logo, use_column_width=True)


    if upload_file is not None and Path(upload_file.name).suffix == '.csv':
        df = pd.read_csv(upload_file, encoding='unicode_escape')
        st.dataframe(df, width=1800)

    if upload_file is not None and Path(upload_file.name).suffix == '.xlsx':
        df = pd.read_excel(upload_file)
        st.dataframe(df, width=1800)




    with st.sidebar:
        st.title('Datos de la factura')
        st.text_input('Nombre de la empresa', key="company_name")
        st.text_input('Nombre del vendedor', key="seller_name")
        st.text_input('Website del vendedor', key="seller_website")
        st.text_input('RUC del vendedor', key="seller_ruc")

        st.text_input('Nombre del cliente', key="client_name")


        st.text_input('Fecha de la factura', key="date")

        st.text_input('Concepto de la factura', key="concept")

        st.file_uploader('Ingresar logo de la empresa', type=['png', 'jpg'], key="company_logo")


        st.write("company_name", "✅" if st.session_state.seller_name else "❌")
        st.write("seller name", "✅" if st.session_state.seller_name else "❌")
        st.write("seller ruc", "✅" if st.session_state.seller_ruc else "❌")
        st.write("client name", "✅" if st.session_state.client_name else "❌")
        st.write("date", "✅" if st.session_state.date else "❌")
        st.write("concept", "✅" if st.session_state.concept else "❌")
        st.write("company_logo", "✅" if st.session_state.company_logo else "❌")
        st.write("seller_website", "✅" if st.session_state.seller_website else "❌")


if __name__ == '__main__':
    main()
