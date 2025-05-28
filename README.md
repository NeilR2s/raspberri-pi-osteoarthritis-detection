# Model Card: Osteoarthritis Screening System 

**Table of Contents**

- [Model details](#model-details)
- [Intended use](#intended-use)
- [Factors](#factors)
- [Metrics](#metrics)
- [Training data](#training-data)
- [Quantitative analyses](#quantitative-analyses)
- [Ethical considerations](#ethical-considerations)
- [Caveats and recommendations](#caveats-and-recommendations)

## Model details

- **Model Name:** tf-osteo
- **Developer:** Neil Artus (*model training and inference*), Joshua Lawrence C. Contreras (*user interface*)
- **Researchers:**  Joshua Lawrence C. Contreras, Hadji Luis L. Montealegre, Francis G. Yaeso
- **Model version:** 1.0
- **Model type:** Convolutional Neural Network (CNN) for image classification based on the MobileNetV3 architecture with custom (BatchNormalization, Dropout,  Dense) layers.
- **Paper Title:** "Development of an Osteoarthritis Screening System using Convolutional Neural Network (CNN) Algorithm and Infrared Thermography (IRT)" - *Undergraduate Thesis, Lyceum of the Philippines University-Cavite* 
- **Citation details:** Contreras, J.L.C., Montealegre, H.L.L., & Yaeso, F.G. (2024). Development of an Osteoarthritis Screening System using Convolutional Neural Network (CNN) Algorithm and Infrared Thermography (IRT). Lyceum of the Philippines University-Cavite.
- **License:** GNU Affero General Public License v3.0
- Contact Details for Queries: neil.c.artus@gmail.com

## Intended use

### Primary intended uses
- To serve as a cost-effective screening tool for early detection of knee osteoarthritis (OA), specifically focusing on Kellgren-Lawrence (KL) grades 0 to 3
- To classify thermal images of knee joints into OA severity grades based on the KL grading system.
- To be used by healthcare professionals (rheumatologists, orthopedic specialists) as an aid in OA screening and assessment, particularly in clinical settings like the ACC Orthopedic and Physical Therapy Clinic.
### Primary intended users
- Healthcare professionals specializing in osteoarthritis diagnosis and treatment.
- Researchers in medical imaging and AI for healthcare.

### Out-of-scope use cases
- Not intended as a standalone diagnostic tool to replace X-rays, MRIs, or expert clinical judgment. It is a screening system.
- Not validated for use on other joints besides the knee.
- Not validated for pediatric use.
- Not intended for self-diagnosis by patients without professional medical consultation.
- The model's performance on KL grades 3, while potentially classifiable, is not the primary focus for early detection as per the thesis scope.
  
## Factors

### Relevant factors
- Demographics: Age, sex, Body Mass Index (BMI) are known risk factors for KOA. The model's performance might vary across different demographic groups.
- Environmental Conditions for IRT: Room temperature (target 22°C ±1°C), humidity (target constant), absence of direct sunlight, and patient resting time (target 20 min ± 3 min) are crucial for consistent thermal image acquisition. Deviations may affect image quality and model performance.
- Image Acquisition: Angle of external foot rotation (target 15°) and Region of Interest (ROI) selection consistency. Variations in camera (FLIR Lepton Radiometric Camera Module positioning and ROI extraction can impact results.

### Technical Factors 
- Image resolution (224x224 input), thermal noise.
  
## Metrics
- Accuracy: Overall classification accuracy. Target validation accuracy was 87.8%. Achieved validation accuracy was 99.40% at epoch 100. Test accuracy was 98.19%.
- Loss: Sparse Categorical Crossentropy.

### Decision thresholds
- Softmax output of final dense layer, argmax for inference.
  
### Datasets
Thermal images of knee joints from patients diagnosed with osteoarthritis.
Source: ACC Orthopedic and Physical Therapy Clinic (Noveleta, Cavite City, Bacoor, Imus).
**Training:** 1572 files belonging to 4 classes. **Validation:** 332 files belonging to 4 classes. **Test:** 332 files belonging to 4 classes.

### Motivation
To develop a cost-effective OA screening tool using IRT and CNN, focusing on early detection.

### Preprocessing
- Images resized to 224x224 pixels.
- Color mode: RGB
  
## Training data
**Data Augmentation:** RandomFlip, RandomZoom , RandomContrast , RandomTranslation, GaussianNoise

## Quantitative analyses

### Results

- **Validation Accuracy:** 99.40% (at epoch 100).
- **Test Accuracy:** 98.19%.
  
### Training Hyperparameters
- **Optimizer:** Adamax (learning_rate = 0.0001)
- **Loss Function:** sparse_categorical_crossentropy
- **Batch Size:** 16
- **Epochs: 100** (with early stopping patience=8, monitoring 'val_loss')
- **Base Model:** MobileNetV3Small (*Trainable*)
- **Regularizers:** L2 (kernel), L1 (activity, bias) on the dense layer.
- **Dropout Rate:** 0.4

## Ethical considerations

### Data Privacy & Consent:

Patient data (and by extension the dataset) is confidential and therefore not accessible.
Informed consent from patients was obtained for data collection and use in research.

### Potential Biases:

Dataset Bias: Data collected from specific clinics in Cavite, Philippines. Model performance may vary on populations with different demographic characteristics, OA etiologies, or thermal presentation. Thesis notes potential limitation in statistical significance due to small sample size from clinic's limited patient population.

### Intended Use & Misuse:

- The system is intended as a screening aid for healthcare professionals, not a definitive diagnostic tool.
- Misuse could involve over-reliance on the model's output without clinical correlation or use for self-diagnosis. User training and clear communication of the tool's capabilities and limitations are important.
- Impact on Vulnerable Groups: The study aims to improve accessibility, especially in remote or low-income areas, aligning with SDG 10 (Reduced Inequalities).

## Caveats and recommendations

- Model performance is dependent on the quality and characteristics of the training data. Performance on out-of-distribution data (e.g., different camera types, significantly different patient populations, or environmental conditions) is not guaranteed.

- Limited sample size from specific clinics may affect generalizability.

- Thermal imaging detects temperature variations associated with inflammation, not direct structural changes. It should complement, not replace, other diagnostic modalities like X-ray or MRI for definitive OA diagnosis.

- High validation/test accuracy; this warrants investigation for potential overfitting or issues with the test set diversity.
