# ==============================================================
# Author: Rodolfo Ferro
# Twitter: @FerroRodolfo
#
# ABOUT COPYING OR USING PARTIAL INFORMATION:
# This script has been originally created by Rodolfo Ferro.
# Any explicit usage of this script or its contents is granted
# according to the license provided and its conditions.
# ==============================================================

# -*- coding: utf-8 -*-

import streamlit as st
import numpy as np
import requests
from PIL import Image


st.sidebar.title("Computer Vision API")
st.sidebar.markdown(
    """
    In this simple app you can test your _Computer Vision_ of Microsoft Azure.
    
    """
)
api_key = st.sidebar.text_input('API Key')
endpoint = st.sidebar.text_input('Endpoint')


st.title("Image Analysis with Computer Vision API")
st.markdown(
    """
    Below you can explore the results of the image analysis which 
    has the Microsoft Azure Computer Vision API. In the next block 
    you can upload an image from your computer anduse your own API 
    Computer Vision to perform an analysis of it. 
    """
)

valid_formats = ['png', 'jpg', 'jpeg']
upfile = st.file_uploader('Please upload an image.', type=valid_formats)
if upfile is not None:
    img_bytes = upfile.read()
    img = Image.open(upfile)
    img = np.array(img).astype('uint8')
    st.image(img, caption='Image uploaded .')


if st.button('Process image with Computer Vision API'):
    # Verify keys and values
    if upfile is None:
        st.error('You must upload an image.')

    if api_key == '':
        st.error('You must enter an API Key.')
    
    if endpoint == '':
        st.error('You must enter a valid endpoint.')
    
    if upfile and api_key and endpoint:
        # Create metadata for Computer Vision API
        analyze_url = endpoint + 'vision/v3.1/analyze'
        headers = {
            'Ocp-Apim-Subscription-Key': api_key,
            'Content-Type': 'application/octet-stream'
        }
        params = {
            'visualFeatures': 'Categories,Description,Color'
        }

        response = requests.post(
            analyze_url,
            headers=headers,
            params=params,
            data=img_bytes
        )
        response.raise_for_status()
        analysis = response.json()

        image_caption = analysis['description']['captions'][0]['text']
        image_caption = image_caption.capitalize()

        tags = analysis['description']['tags']
        items = [f'\n- {tag}' for tag in tags]
        items = ''.join(items)
        
        st.markdown(
            f"""
            ## Image analysis results

            **JSON file response:**
            ```json
            {analysis}
            ```

            **Description of Computer Vision API:**
            _"{image_caption}"_.
            """
        )

        st.markdown(
            f"""
            **Tags of items detected:**
            {items} 
            """
        )
