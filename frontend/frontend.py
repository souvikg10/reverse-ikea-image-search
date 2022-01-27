import streamlit as st
from config import IMAGE_PORT, IMAGE_SERVER, DEBUG, TEXT_PORT, TEXT_SERVER, TEXT_SAMPLES
from helper import search_by_file, UI, convert_file_to_document, get_image_url
from PIL import Image

matches = []

# Layout
st.set_page_config(page_title="IKEA search")
st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)
st.write(
    "<style>div.row-widget.stRadio > div{flex-direction:row; margin-left:auto; margin-right: auto; align: center}</style>",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.markdown(UI.about_block, unsafe_allow_html=True)

if DEBUG:
    with st.sidebar.expander("Debug"):
        TEXT_SERVER = st.text_input(label="Text server", value=TEXT_SERVER)
        TEXT_PORT = st.text_input(label="Text port", value=TEXT_PORT)
        IMAGE_SERVER = st.text_input(label="Image server", value=IMAGE_SERVER)
        IMAGE_PORT = st.text_input(label="Image port", value=IMAGE_PORT)

st.header("Search IKEA Images")

upload_cell, preview_cell = st.columns([12, 1])
query = upload_cell.file_uploader("")
if query:
    doc = convert_file_to_document(query)
    image = Image.open(query)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    if st.button(label="Search"):
        if not query:
            st.markdown("Please enter a query")
        else:
            matches = search_by_file(document=doc, server=IMAGE_SERVER, port=IMAGE_PORT)

# Results area
cell1, cell2, cell3 = st.columns(3)
cell4, cell5, cell6 = st.columns(3)
cell7, cell8, cell9 = st.columns(3)
cell10, cell11, cell12 = st.columns(3)
cell13, cell14, cell15 = st.columns(3)
all_cells = [
    cell1,
    cell2,
    cell3,
    cell4,
    cell5,
    cell6,
    cell7,
    cell8,
    cell9,
    cell10,
    cell11,
    cell12,
    cell13,
    cell14,
    cell15,
]


for cell, match in zip(all_cells, matches):
    cell.image(get_image_url(match.uri))
    for k, v in match.tags["file"].__dict__.items():
        cell.text(v.fields["file_name"].string_value.split("/")[1])
        cell.text(f'{match.scores["cosine"].value:2f}')
