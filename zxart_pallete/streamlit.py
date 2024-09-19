import io
import tomllib

import streamlit as st
from PIL import Image

from zxart_pallete import zxart


def pallete_list() -> list[str]:
    return list(tomllib.loads(zxart.PALLETES_TOML.read_text()).keys())


palletes = pallete_list()

st.title("ZXArt Pallete")

image_file = st.file_uploader("Image")
if image_file:
    st.image(image_file)

pallete_name = st.selectbox("Pallete", palletes)

processed = st.button("Colorize")
if processed:
    if not image_file:
        st.error("Need to upload file")
    elif not pallete_name:
        st.error("Need to select pallete")
    else:
        image_io = io.BytesIO(image_file.getvalue())
        image = Image.open(image_io)
        pallete = zxart.loaded_pallete(pallete_name)
        try:
            result = zxart.colorized_image(image, pallete)
            st.image(result)
        except ValueError as e:
            st.error(f"Error: {e}")

