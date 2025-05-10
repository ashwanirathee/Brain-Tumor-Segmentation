import base64
import io
import numpy as np
import requests
from PIL import Image
from dash import html, exceptions, Dash, dcc, no_update
import xml.etree.ElementTree as ET
import numpy as np
from skimage import data
import plotly.express as px
import skimage.io as sio
import matplotlib.pyplot as plt
import vtracer
from svgpathtools import parse_path
from svgpathtools.path import Path
import re

def parse_contents(contents, server_type):
    data = contents.split(",")[1]
    img_bytes = base64.b64decode(data)
    imgdata = Image.open(io.BytesIO(img_bytes))

    img_buffer = io.BytesIO()
    imgdata.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    # Send to prediction server
    if server_type == "GCP server":
        url = "https://julia-braintumorseg.et.r.appspot.com/predict"
    elif server_type == "Heroku Server":
        url = "https://brain-segment-api.herokuapp.com/predict"
    else:
        url = "http://localhost:5001/predict"

    resp = requests.post(url, files={"file": ("image.png", img_buffer, "image/png")})

    if resp.status_code != 200:
        raise ValueError(f"Error: {resp.status_code} - {resp.text}")
    json_load = resp.json()
    mask = ~np.asarray(json_load["mask"])
    mask_img = (mask.astype(np.uint8)) * 255
    mask_pil = Image.fromarray(mask_img)

    buffer = io.BytesIO()
    mask_pil.save(buffer, format="PNG")
    encoded_image = base64.b64encode(buffer.getvalue()).decode()
    input_img_bytes: bytes = buffer.getvalue() # e.g. reading bytes from a file or a HTTP request body
    svg_str: str = vtracer.convert_raw_image_to_svg(input_img_bytes, img_format = 'PNG', colormode = 'bw')
    return imgdata, html.Img(src=contents), html.Img(src=f"data:image/png;base64,{encoded_image}"), mask_pil, svg_str

def update_output(list_of_contents, server_type):
    if list_of_contents is None:
        print("Update output stage: No update")
        return no_update, no_update, no_update

    # Parse and get original + mask image
    imgdata, input_image, output_image, mask_pil, svg_str = parse_contents(list_of_contents[0], server_type)
    fig = px.imshow(np.array(imgdata.convert("RGB")))

    svg_root = ET.fromstring(svg_str)

    # Namespace
    ns = {"svg": "http://www.w3.org/2000/svg"}

    # Loop through <path> elements
    for path_elem in svg_root.findall(".//svg:path", namespaces=ns):
        fill_color = path_elem.attrib.get("fill")
        if fill_color != "#000000":
            continue

        d = path_elem.attrib.get("d")
        transform = path_elem.attrib.get("transform", "")

        if d:
            path_obj = parse_path(d)

            # Apply translation if present
            if "translate" in transform:
                match = re.search(r"translate\(([^,]+),([^)]+)\)", transform)
                if match:
                    dx, dy = float(match.group(1)), float(match.group(2))
                    path_obj = path_obj.translated(complex(dx, dy))

            # Rebuild path string
            translated_d = path_obj.d()

            # Add to Plotly
            fig.add_shape(
                editable=True,
                type="path",
                path=translated_d + " Z",
                line_color="SkyBlue",
                line_width=5,
            )


    fig.update_layout(
        dragmode="drawrect",
        newshape=dict(line_color="cyan"),
        width=500,
        height=500,
    )

    update_graph = dcc.Graph(
        figure=fig.update_layout(
            plot_bgcolor="#f9f9f9",  # inside plot area
            paper_bgcolor="#ffffff"  # entire figure background
        ),
        config={
            "modeBarButtonsToAdd": [
                "drawline",
                "drawopenpath",
                "drawclosedpath",
                "drawcircle",
                "drawrect",
                "eraseshape",
            ]
        },
        className="divgraph",
        style={
            "backgroundColor": "#ffffff",  # sets the container background
            "height": "100%",              # make it fill available vertical space
            "width": "100%",               # make it fill available horizontal space
            "border": "1px solid #ccc"     # optional border
        }
    )

    print("Update output stage: New update")
    return input_image, output_image, update_graph


def save_file(n_clicks):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    else:
        return dcc.send_file("./mask.png")
