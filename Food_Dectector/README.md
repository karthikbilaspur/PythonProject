# Food Detector

Model: VGG16 with custom classification layers
Dataset: Food images with 10 classes
Training:
Data augmentation: shear, zoom, horizontal flip
Batch size: 32
Epochs: 10
Evaluation:
Test accuracy: printed
Classification report: printed
Confusion matrix: printed
Detection:
Function: detect_food takes an image path as input
Returns: predicted class label
Key Features:
Image preprocessing and data augmentation
Model evaluation and performance metrics
Detection function for new images.
