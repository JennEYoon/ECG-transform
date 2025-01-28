# ECG classification using deep learning 

The repository contains the code for the experiments presented in the paper [Leinonen et al. (2024), "Empirical investigation of multi-source cross-validation in clinical ECG classification"](https://doi.org/10.1016/j.compbiomed.2024.109271).

PyTorch implementations of two PhysioNet Challenge 2020 models are provided: the ResNet model from [Zhao et al.](https://moody-challenge.physionet.org/2020/papers/112.pdf) and the Transformer model from [Natarajan et al.](https://www.cinc.org/archives/2020/pdf/CinC2020-107.pdf). Additionally, code for benchmark models, specifically Logistic regression and XGBoost, is available. 

The repository has been refactored for a more generalized approach to ECG analysis. The initial code for the neural networks can be found, for example, [here](https://moody-challenge.physionet.org/2020/results/).

There are three branches, each containining either the neural network pipeline or a script to run the benchmark models
- The `main` branch contains the ResNet pipeline
- The `benchmark_models` branch includes the Logistic regression model and the XGBoost model
- The `ecg_property_study` branch contains an updated ResNet pipeline that includes more sophisticated ECG data modification.
- The `transformer_network` contains the Transformer pipeline:

The two neural network pipelines are run similarly as described below using YAML files to read the training or testing configurations from, and the CSV files to read the data from. The transformer model also incorporates handfracted features extracted from ECGs which are stored as CSV files in `data/features`. Benchmark models are run using the ipynb script.

# Usage

To get started, install the required Python packages from the `requirements.txt` file using the following command:

```
pip install -r requirements.txt
```

The repository is tested with the Python version 3.10.4.

For feature extraction regarding the Transformer model and the benchmark models, the [PyEEG module](https://github.com/forrestbao/pyeeg/tree/master) is also required. The functions are assumed to be located to `src/features/pyeeg`. 

# Data

For detailed information on how to download, preprocess, and split the data, please check out the [Setup the runs](/notebooks/1_setup_runs.ipynb) notebook in the `/notebooks/` directory.


# In a nutshell

If you wish to preprocess the data, you can use the `preprocess_data.py` script. Although not mandatory for repository usage, note that certain transforms, such as BandPassFilter, may significantly slow down training. To preprocess the data, execute the following command:

```
python preprocess_data.py
```

You can find YAML configurations in the `configs` directory:

* YAML files in the `training` directory are used for training a model
* YAML files in the `predicting` directory are used for testing and evaluating a model.

Two notebooks are available for creating training and testing YAML files based on the data splitting performed with the `create_data_csvs.py` script: [Yaml files of database-wise split for training and testing](/notebooks/2_physionet_DBwise_yaml_files.ipynb) and [Yaml files of stratified split for training and testing](/notebooks/2_physionet_stratified_yaml_files.ipynb). In addition, the `create_yaml_files.py` script is another option to create the YAML files. Be sure to perform the data splitting first.

1) To split the data for model training and testing, run the following command:

```
python create_data_csvs.py
```

This script uses either stratified split or database-wise split. Stratified split employs either ShuffleSplit or K-Fold cross validation techniques to generate CSV files, including the files for a training set and a validation set. These CSV files have columns for ECG recording `path`, `age`, `gender`, and all diagnoses in SNOMED CT codes used as labels in classification. CSV files for test data are also generated. Database-wise split utilizes the directory structure where the data is loaded from.

The primary structure of the CSV files is as follows:


| path  | age  | gender  | 10370003  | 111975006 | 164890007 | *other diagnoses...* |
| ------------- |-------------|-------------| ------------- |-------------|-------------|-------------|
| ./Data/A0002.mat | 49.0 | Female | 0 | 0 | 1 | ... |
| ./Data/A0003.mat | 81.0 | Female | 0 | 1 | 1 | ... |
| ./Data/A0004.mat | 45.0 |  Male  | 1 | 0 | 0 | ... |
| ... | ... |  ...  | ... | ... | ... | ... |


Note: There are attributes to consider before running the script. Please check out the [Introduction to data handling](/notebooks/1_introduction_data_handling.ipynb) notebook for further instructions.

2) To train a model, use either a YAML file or a directory as an argument with one of the following commands:

```
python train_model.py train_smoke.yaml
python train_model.py train_stratified_smoke
```

The `train_data.yaml` file contains necessary training arguments in YAML format, while `train_multiple_smoke` is a directory containing several YAML files. When using multiple YAML files, each file is loaded and executed separately. For more detailed training information, check the [Introduction to training models](/notebooks/3_introduction_training.ipynb) notebook.

3) To test and evaluate a trained model, use one of the following commands:

```
python run_model.py predict_smoke.yaml
python run_model.py predict_stratified_smoke
```

 Similar to training, the `predict_smoke.yaml` file contains necessary arguments for the prediction phase in YAML format, while `predict_multiple_smoke` is a directory with multiple YAML files. When using multiple YAML files, each file is loaded and executed separately. Detailed information about prediction and evaluation is available in the [Introduction to testing and evaluating models](/notebooks/4_introduction_testing_evaluation.ipynb) notebook.


# Repository structure

```
.
├── configs                      
│   ├── data_splitting           # Yaml files considering a database-wise split and a stratified split   
│   ├── predicting               # Yaml files considering the prediction and evaluation phase
│   └── training                 # Yaml files considering the training phase
│   
├── data
│   ├── smoke_data               # Samples from the Physionet 2021 Challenge data as well as
|   |                              Shandong Provincial Hospital data for smoke testing
│   └── split_csvs               # Csv files of ECGs, either database-wise or stratified splitted
│
├── notebooks                    # Jupyter notebooks for data exploration and 
│                                  information about the use of the repository
├── src        
│   ├── dataloader 
│   │   ├── __init__.py
│   │   ├── dataset.py           # Script for custom DataLoader for ECG data
│   │   ├── dataset_utils.py     # Script for preprocessing ECG data
│   │   └── transforms.py        # Script for tranforms
│   │
│   └── modeling 
│       ├── models               # All model architectures
│       │   └── seresnet18.py    # PyTorch implementation of the SE-ResNet18 model
│       ├──__init__.py
│       ├── metrics.py           # Script for evaluation metrics
│       ├── predict_utils.py     # Script for making predictions with a trained model
│       └── train_utils.py       # Setting up optimizer, loss, model, evaluation metrics
│                                  and the training loop
│
├── .gitignore
├── LICENSE
├── LICENSE.txt
├── README.md
├── __init__.py
├── create_data_csvs.py          # Script to perform either database-wise data split or
│                                  split by stratified K-fold or ShuffleSplit
├── create_yaml_files.py         # Script to create YAML files for configurations
├── label_mapping.py             # Script to convert other diagnostic codes to SNOMED CT Codes
├── preprocess_data.py           # Script for preprocessing data
├── README.md
├── requirements.txt             # The requirements needed to run the repository
├── run_model.py                 # Script to test and evaluate a trained model
├── train_model.py               # Script to train a model
└── utils.py                     # Script for YAML configuration

```

# Citation

```
@article{leinonen2024empirical,
  title={Empirical investigation of multi-source cross-validation in clinical ECG classification},
  author={Leinonen, Tuija and Wong, David and Vasankari, Antti and Wahab, Ali and Nadarajah, Ramesh and Kaisti, Matti and Airola, Antti},
  journal={Computers in Biology and Medicine},
  volume={183},
  pages={109271},
  year={2024},
  publisher={Elsevier}
}
```
