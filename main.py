from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
import streamlit as st
import os
import tempfile
from dateutil import parser
import base64
from PIL import Image
import docx



st.title("Metadata file extractor")

uploaded_file = st.file_uploader("File upload")
if uploaded_file:
    with st.spinner('Cargando datos ...'):
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        if uploaded_file.type == 'application/pdf':
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            fp = open(path, 'rb')
            parsed_file = PDFParser(fp)
            doc = PDFDocument(parsed_file)

            for element in doc.info[0]:
                try:
                    if "Date" in element:
                        element_val =  element_val = parser.parse(doc.info[0][element].decode('utf-8')[2:14])
                        st.write(f"**{element}:** {element_val}")
                    else:
                        try:
                            element_val = doc.info[0][element].decode('utf-8')
                            st.markdown(f"**{element}:** {element_val}")
                        except:
                            element_val = doc.info[0][element].decode('utf-16')
                            st.markdown(f"**{element}:** {element_val}")
                except:
                    pass


            with st.expander("RAW data"):
                st.write(doc.info[0])
        

            with st.expander("PDF file"):
                with open(path, "rb") as f:
                    base64_pdf = base64.b64encode(f.read()).decode('utf-8')
                pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

                    
                st.markdown(pdf_display, unsafe_allow_html=True) 
        elif uploaded_file.type == 'image/jpeg' or uploaded_file.type == 'image/png':
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
            image = Image.open(path)
            exif_data = image._getexif()
            for element in exif_data:
                if element == 256:
                    element_txt = "Width"
                    element_val = exif_data[element]
                elif element == 257:
                    element_txt = "Height"
                    element_val = exif_data[element]
                elif element == 274:
                    element_txt = "Orientation"
                    element_val = exif_data[element]
                elif element == 270:
                    element_txt = "ImageDescription"
                    element_val = exif_data[element]
                elif element == 306:
                    element_txt = "Date"
                    element_val = exif_data[element]
                else:
                    element_txt = element
                    element_val = exif_data[element]

                st.markdown(f"**{element_txt}:** {element_val}")
                #st.markdown(f"**{element}:** {exif_data[element]}")
            
            st.image(image)
            with st.expander("RAW data"):
                st.write(exif_data)

        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            with open(path, "wb") as f:
                f.write(uploaded_file.getvalue())
                doc = docx.Document(path)
                title = doc.core_properties.title
                st.markdown(f"**Title:** {title}")

                author = doc.core_properties.author
                st.markdown(f"**Author:** {author}")

                created = doc.core_properties.created
                st.markdown(f"**Created:** {created}")

                modified = doc.core_properties.modified
                st.markdown(f"**Modified:** {modified}")

                category = doc.core_properties.category
                st.markdown(f"**Category:** {category}")

                comments = doc.core_properties.comments
                st.markdown(f"**Comments:** {comments}")

                identifier = doc.core_properties.identifier
                st.markdown(f"**Identifier:** {identifier}")

                keyworks = doc.core_properties.keywords
                st.markdown(f"**Keyworks:** {keyworks}")

                language = doc.core_properties.language
                st.markdown(f"**Language:** {language}")

                last_modified_by = doc.core_properties.last_modified_by
                st.markdown(f"**Last modified by:** {last_modified_by}")


                subject = doc.core_properties.subject
                st.markdown(f"**Subject:** {subject}")

                version = doc.core_properties.version
                st.markdown(f"**Version:** {version}")

                revision = doc.core_properties.revision
                st.markdown(f"**Revision:** {revision}")

                subject = doc.core_properties.subject
                st.markdown(f"**Subject:** {subject}")

        else:
            st.write(f" {uploaded_file.type} file type not supported")


            
