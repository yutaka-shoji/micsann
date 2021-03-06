# micsann

*micsann* is a small Python package to calculate the temperature response function of the MICS-ANN (Moving Infinite Cylindrical Source) model.

## Quick start

### On Google Colab

Just run quickstart.ipynb on Google Colab.   
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yutaka-shoji/micsann/blob/main/quickstart.ipynb)

### Local Install

Download this repository.

Git users may also clone this repository with the following command:

```sh
$ git clone https://github.com/yutaka-shoji/micsann.git
```

Run the installation script in the downloaded directory:

```sh
$ python setup.py install
```

You can import the *micsann* library in your Python environment.

Bundled *quickstart.py* calculates and visualizes the temperature response function of the MICS-ANN model.

```sh
$ python quickstart.py
```

Resulted Figure

<img src="https://user-images.githubusercontent.com/52145911/114144828-b4854b80-9950-11eb-8f9c-a4f9a43f58c3.png" width=50%>

## Requirements

*micsann* needs following modules in Python3.

- [numpy](https://numpy.org)
- [pandas](https://pandas.pydata.org)
- torch ([PyTorch](https://pytorch.org))
- [matplotlib](https://matplotlib.org) (for quickstart.py visualize)

## Citations

For a detailed description of the MICS-ANN model, please refer to the following journal article.
> Shoji, Y., Katsura, T., Nagano, K., 2022. MICS-ANN model: An artificial neural network model for fast computation of G-function in moving infinite cylindrical source model. Geothermics 100, 102315–102315. https://doi.org/10.1016/j.geothermics.2021.102315
