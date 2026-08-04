# 🌍 Urban Heat Mapping via Roof Type Classification

An AI-powered system for analyzing **Urban Heat Island (UHI)** effects by combining **rooftop segmentation, roof type classification, and thermal mapping** using satellite imagery.

The project uses **YOLOv8** for rooftop segmentation, **Land Surface Temperature (LST)** data for rooftop temperature estimation, and an interactive **Streamlit dashboard** to visualize heat distribution and support sustainable urban planning.

---

## 📌 Project Overview

Urban Heat Islands occur when urban regions experience higher temperatures than surrounding rural areas due to dense infrastructure and reduced vegetation.

This project automates the analysis of rooftop heat patterns by:

- Detecting rooftops from satellite imagery
- Classifying roof types
- Estimating rooftop temperatures using LST data
- Visualizing thermal hotspots through an interactive dashboard

---

## ✨ Features

- 🛰️ Rooftop Segmentation using YOLOv8
- 🏠 Roof Type Classification
- 🌡️ Land Surface Temperature (LST) Analysis
- 📊 Rooftop Temperature Statistics
- 🔥 Thermal Heatmap Visualization
- 📈 Interactive Charts and Tables
- 💻 Streamlit Dashboard for Real-time Analysis

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Deep Learning
- YOLOv8 (Ultralytics)
- TensorFlow / Keras
- PyTorch

### Libraries
- OpenCV
- NumPy
- Pandas
- Matplotlib
- Rasterio
- Pillow
- Scikit-learn

### Dashboard
- Streamlit

### Annotation Tool
- Roboflow

### Development Environment
- Google Colab
- VS Code
- Git & GitHub

---

## 📂 Project Structure

```text
Urban-Heat-Mapping-via-Roof-Type-Classification
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/
│   └── bangalore_lst.tif
│
├── models/
│   └── best.pt
│
├── notebooks/
│
├── outputs/
│
├── sample_images/
│
└── docs/
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/monishasrinivas-04/Urban-Heat-Mapping-via-Roof-Type-Classification.git
```

Move into the project directory:

```bash
cd Urban-Heat-Mapping-via-Roof-Type-Classification
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit dashboard:

```bash
streamlit run app.py
```

---

## 🚀 Workflow

```text
Satellite Image
        │
        ▼
YOLOv8 Rooftop Segmentation
        │
        ▼
Roof Detection
        │
        ▼
Roof Type Classification
        │
        ▼
Land Surface Temperature Analysis
        │
        ▼
Heatmap Generation
        │
        ▼
Interactive Streamlit Dashboard
```

---

## 📊 Results

The project provides:

- Accurate rooftop detection from satellite imagery
- Rooftop temperature estimation using LST data
- Heat distribution analysis
- Interactive visualizations for Urban Heat Island assessment

---

## 🔮 Future Enhancements

- Green Roof Detection
- Solar Rooftop Suitability Analysis
- GIS Map Integration
- Real-time Satellite Data Processing
- Building-wise Heat Risk Assessment
- Carbon Emission and Cooling Impact Analysis

---

## 👩‍💻 Author

**Monisha S**

B.Tech – Artificial Intelligence & Machine Learning

M. S. Ramaiah University of Applied Sciences

GitHub: https://github.com/monishasrinivas-04

---

## ⭐ Acknowledgements

- AICTE
- Edunet Foundation
- Shell India
- Ultralytics
- Roboflow
- Streamlit