import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Website Image Extractor", layout="wide")
st.title("🖼️ Website Image Extractor")

url = st.text_input("Enter the URL of the website:")

if url:
    with st.spinner("Fetching and parsing images..."):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            images = soup.find_all("img")

            if not images:
                st.warning("No images found on this page.")
            else:
                st.success(f"Found {len(images)} image(s). Displaying them below:")
                for i, img_tag in enumerate(images):
                    img_src = img_tag.get("src")
                    if not img_src:
                        continue
                    img_url = urljoin(url, img_src)
                    try:
                        img_data = requests.get(img_url).content
                        image = Image.open(BytesIO(img_data))
                        st.image(image, caption=img_url, use_column_width=True)
                    except Exception as e:
                        st.error(f"Failed to load image: {img_url}\nError: {e}")

        except Exception as e:
            st.error(f"Failed to fetch the URL: {e}")

st.markdown("---")
st.caption("Built with ❤️ using Streamlit")