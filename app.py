import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import rasterio
import cv2

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="UHSI Rooftop Dashboard",
    layout="wide"
)

st.title("Urban Heat Island Rooftop Analysis Dashboard")

# -----------------------------------
# LOAD YOLO MODEL
# -----------------------------------

model = YOLO(
    r"models/best.pt"
)

# -----------------------------------
# LOAD LST TIFF FILE
# -----------------------------------

lst_path = r"data/bangalore_lst.tif"

with rasterio.open(lst_path) as src:
    lst_data = src.read(1)

# Remove NaN values
lst_data = np.nan_to_num(lst_data)

# Normalize thermal image
lst_normalized = cv2.normalize(
    lst_data,
    None,
    0,
    255,
    cv2.NORM_MINMAX
)

lst_normalized = np.uint8(lst_normalized)

# -----------------------------------
# SIDEBAR CONTROLS
# -----------------------------------

st.sidebar.header("Dashboard Controls")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    0.1,
    1.0,
    0.5
)

# -----------------------------------
# IMAGE UPLOAD
# -----------------------------------

uploaded_file = st.file_uploader(
    "Upload Satellite Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:

    # FIXED RGB CONVERSION
    image = Image.open(uploaded_file).convert("RGB")

    image_np = np.array(image)

    st.subheader("Uploaded Satellite Image")

    st.image(
        image,
        use_container_width=True
    )

    # -----------------------------------
    # YOLO PREDICTION
    # -----------------------------------

    results = model.predict(
        source=image_np,
        conf=confidence,
        save=False,
        show_labels=False,
        show_conf=False
    )

    result = results[0]

    plotted = result.plot()

    st.subheader("Detected Rooftops")

    st.image(
        plotted,
        use_container_width=True
    )

    # -----------------------------------
    # TEMPERATURE ANALYSIS
    # -----------------------------------

    temperatures = []

    total_roofs = 0

    if result.boxes is not None:

        boxes = result.boxes.xyxy.cpu().numpy()

        total_roofs = len(boxes)

        for box in boxes:

            x1, y1, x2, y2 = map(int, box)

            # Prevent overflow
            x1 = max(0, x1)
            y1 = max(0, y1)

            x2 = min(lst_normalized.shape[1], x2)
            y2 = min(lst_normalized.shape[0], y2)

            roi = lst_normalized[y1:y2, x1:x2]

            if roi.size > 0:

                temp = np.mean(roi)

                temperatures.append(temp)

    # -----------------------------------
    # DASHBOARD METRICS
    # -----------------------------------

    avg_temp = np.mean(temperatures) if temperatures else 0

    hottest_temp = np.max(temperatures) if temperatures else 0

    coolest_temp = np.min(temperatures) if temperatures else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Rooftops",
        total_roofs
    )

    col2.metric(
        "Average Roof Temperature",
        f"{avg_temp:.2f}"
    )

    col3.metric(
        "Hottest Roof",
        f"{hottest_temp:.2f}"
    )

    col4.metric(
        "Coolest Roof",
        f"{coolest_temp:.2f}"
    )

    # -----------------------------------
    # TEMPERATURE HISTOGRAM
    # -----------------------------------

    st.subheader("Roof Temperature Distribution")

    fig1, ax1 = plt.subplots(figsize=(8, 4))

    ax1.hist(
        temperatures,
        bins=10
    )

    ax1.set_xlabel("Temperature")

    ax1.set_ylabel("Number of Roofs")

    st.pyplot(fig1)

    # -----------------------------------
    # PIE CHART
    # -----------------------------------

    st.subheader("Roof Heat Categories")

    hot = len([t for t in temperatures if t > 180])

    medium = len([t for t in temperatures if 120 <= t <= 180])

    cool = len([t for t in temperatures if t < 120])

    fig2, ax2 = plt.subplots()

    ax2.pie(
        [hot, medium, cool],
        labels=["Hot", "Medium", "Cool"],
        autopct="%1.1f%%"
    )

    st.pyplot(fig2)

    # -----------------------------------
    # DATA TABLE
    # -----------------------------------

    st.subheader("Roof Temperature Table")

    df = pd.DataFrame({
        "Roof ID": list(range(1, len(temperatures) + 1)),
        "Temperature": temperatures
    })

    st.dataframe(df)

# -----------------------------------
# LST HEATMAP
# -----------------------------------

st.subheader("Land Surface Temperature Heatmap")

fig3, ax3 = plt.subplots(figsize=(10, 6))

heatmap = ax3.imshow(
    lst_normalized,
    cmap="hot"
)

plt.colorbar(heatmap)

st.pyplot(fig3)