
import os

# Configure writable directories before importing ML/plotting libraries
os.environ["YOLO_CONFIG_DIR"] = "/tmp/Ultralytics"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

from pathlib import Path

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
import cv2
from PIL import Image
from ultralytics import YOLO


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="UHSI Rooftop Dashboard",
    layout="wide"
)

st.title("Urban Heat Island Rooftop Analysis Dashboard")
st.caption("Rooftop detection and exploratory thermal raster visualization")


# -----------------------------------
# PROJECT FILE PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "best.pt"
LST_PATH = BASE_DIR / "data" / "bangalore_lst.tif"


# -----------------------------------
# LOAD YOLO MODEL (CACHED)
# -----------------------------------

@st.cache_resource
def load_model(model_path):
    if not Path(model_path).is_file():
        raise FileNotFoundError(
            f"YOLO model file not found: {model_path}"
        )

    return YOLO(str(model_path))


# -----------------------------------
# LOAD LST RASTER (CACHED)
# -----------------------------------

@st.cache_data
def load_lst(raster_path):
    if not Path(raster_path).is_file():
        raise FileNotFoundError(
            f"LST raster file not found: {raster_path}"
        )

    with rasterio.open(raster_path) as src:
        data = src.read(1, masked=True).filled(np.nan)

    valid = np.isfinite(data)

    if not np.any(valid):
        raise ValueError("The LST raster contains no valid pixels.")

    # Replace invalid pixels with the valid-pixel mean for display.
    display_data = data.copy()
    display_data[~valid] = np.nanmean(data)

    normalized = cv2.normalize(
        display_data,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    return np.uint8(normalized), data


# -----------------------------------
# INITIALIZE RESOURCES
# -----------------------------------

try:
    model = load_model(str(MODEL_PATH))
    lst_normalized, lst_data = load_lst(str(LST_PATH))
except Exception as exc:
    st.error("The dashboard could not initialize its model or raster.")
    st.exception(exc)
    st.stop()


# -----------------------------------
# SIDEBAR CONTROLS
# -----------------------------------

st.sidebar.header("Dashboard Controls")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.1,
    max_value=1.0,
    value=0.5,
    step=0.05
)


# -----------------------------------
# UPLOAD SATELLITE IMAGE
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Satellite Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert("RGB")
        image_np = np.array(image)

        st.subheader("Uploaded Satellite Image")
        st.image(image, use_container_width=True)

        # -------------------------------
        # YOLO PREDICTION
        # -------------------------------

        with st.spinner("Detecting rooftops..."):
            results = model.predict(
                source=image_np,
                conf=confidence,
                save=False,
                verbose=False
            )

        result = results[0]

        # Ultralytics plot output is BGR; convert to RGB for display.
        plotted_bgr = result.plot()
        plotted_rgb = cv2.cvtColor(plotted_bgr, cv2.COLOR_BGR2RGB)

        st.subheader("Detected Rooftops")
        st.image(plotted_rgb, use_container_width=True)

        # -------------------------------
        # ROOFTOP DETECTION SUMMARY
        # -------------------------------

        boxes = (
            result.boxes.xyxy.cpu().numpy()
            if result.boxes is not None
            else np.empty((0, 4))
        )

        total_roofs = len(boxes)

        col1, col2 = st.columns(2)
        col1.metric("Detected Rooftops", total_roofs)
        col2.metric("Confidence Threshold", f"{confidence:.2f}")

        st.info(
            "Thermal comparison is disabled here because the uploaded "
            "image has not been geospatially registered to the Bangalore "
            "LST raster. Pixel coordinates from the two images cannot "
            "safely be assumed to represent the same locations."
        )

    except Exception as exc:
        st.error("Rooftop detection failed.")
        st.exception(exc)


# -----------------------------------
# LST RASTER HEATMAP
# -----------------------------------

st.subheader("Bangalore Land Surface Temperature Raster")

fig, ax = plt.subplots(figsize=(10, 6))

heatmap = ax.imshow(lst_normalized, cmap="hot")
ax.set_xlabel("Raster column (pixel)")
ax.set_ylabel("Raster row (pixel)")
ax.set_title("Normalized raster visualization")

fig.colorbar(heatmap, ax=ax, label="Relative display intensity (0–255)")
st.pyplot(fig)
plt.close(fig)

st.caption(
    "The heatmap uses normalized raster intensities for visualization. "
    "These values are not Celsius temperatures. The raster's units and "
    "calibration must be verified before reporting actual temperatures."
)
