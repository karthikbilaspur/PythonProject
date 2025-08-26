# Adjective Forms Project

This project generates comparative and superlative forms of adjectives using natural language processing (NLP) and machine learning techniques.

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Models](#models)
* [Contributing](#contributing)
* [License](#license)

## Overview

The Adjective Forms Project is a Python-based application that uses NLP and machine learning to generate comparative and superlative forms of adjectives. The project includes both rule-based and machine learning-based approaches to generate adjective forms.

## Features

* Generates comparative and superlative forms of adjectives using rule-based approach
* Trains machine learning models to predict comparative and superlative forms of adjectives
* Trains deep learning models using LSTM networks to predict comparative and superlative forms of adjectives
* Supports both regular and irregular adjectives

## Requirements

* Python 3.8 or higher
* NLTK library
* scikit-learn library
* TensorFlow/Keras library
* pandas library
* numpy library

## Installation

1. Clone the repository: `git clone https://github.com/username/adjective-forms.git`
2. Install the required libraries: `pip install -r requirements.txt`
3. Download the NLTK data: `nltk.download('wordnet')`

## Usage

1. Run the `main.py` file: `python main.py`
2. Enter a list of adjectives when prompted
3. The program will generate comparative and superlative forms of the adjectives using both rule-based and machine learning-based approaches

## Models

The project includes two types of models:

* **Rule-Based Model**: Uses a set of predefined rules to generate comparative and superlative forms of adjectives
* **Machine Learning Model**: Trains a Multinomial Naive Bayes classifier to predict comparative and superlative forms of adjectives
* **Deep Learning Model**: Trains an LSTM network to predict comparative and superlative forms of adjectives

## Contributing

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
