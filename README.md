# Synthetic Knowledge Graphs

This repository provides a collection of code for generating synthetic knowledge graphs. These synthetic knowledge graphs enable practitioners to create controlled scenarios for assessing models and algorithms designed for knowledge graphs.

## Getting Started


To use the datasets and code in this repository, follow these steps:

- Install [Poetry](https://python-poetry.org/) in your system.

- Clone the repository to your local machine.

- Install the dependencies with Poetry.

    ```shell
    poetry install
    ```



## Datasets

Here we enumerate the available synyhetic datasets in this repository, including links to their respective papers, GitHub repositories (if available), associated tests, and script examples for data creation and storage.

**Disclaimer:** We are not the authors that introduced some of the datasets in this repository. We have only implemented the datasets in this repository to have a common interface to interact with them. Please use the links to the original papers for more details about the datasets.



#### FRUNI: Friends and Universities Dataset | [Article](https://openreview.net/forum?id=uU1eXPwesa)

**Associated Tests:** 

To run tests for the FRUNI dataset, use the following command:
```shell
pytest tests/test_fruni.py
```

**Usage Example:** 

To create and work with the FRUNI dataset, execute the following command:
```shell
python scripts/create_fruni.py --name FRUNI_V0 --n_u 100 --lambda_f 1.5 --alpha_u 0.0 --n_f 50
```

#### FTREE: Family Trees Dataset | [Article](https://openreview.net/forum?id=uU1eXPwesa)

**Associated Tests:** 

To run tests for the FTREE dataset, use the following command:
```shell
pytest tests/test_ftree.py
```

**Usage Example:** 

To create and work with the FTREE dataset, execute the following command:
```shell
python scripts/create_ftree.py --name FTREE_V0 --n_t 100 --lambda_b 5.0 --n_d 3
```

#### UserItemAttr: User-Item-Attribute Dataset | [Article](https://arxiv.org/pdf/2302.12465.pdf)  [GitHub](https://github.com/amazon-science/page-link-path-based-gnn-explanation/tree/main)
**Associated Tests:** 

To run tests for the UserItemAttr dataset, use the following command:
```shell
pytest tests/test_user_item_attr.py
```

**Usage Example:** 

To create and work with the FTREE dataset, execute the following command:
```shell
python scripts/create_user_item_attr.py --name UserItemAttr_V0 --num_attrs 20 --num_items 200 --num_users 200 --lambda_a 0.0 --lambda_i 20.0 --percentages 0.8 0.1 0.1 --seed 0 
```


## Citation

If you use the FRUNI or FTREE datasets in your work, please consider citing our [accepted paper](https://openreview.net/forum?id=uU1eXPwesa) at [XAI in Action Workshop @ NeurIPS 2023](https://xai-in-action.github.io/NeurIPS).


```
@inproceedings{
martin2023fruni,
title={{FRUNI} and {FTREE} synthetic knowledge graphs for evaluating explainability},
author={Pablo Sanchez Martin and Tarek Besold and Priyadarshini Kumari},
booktitle={XAI in Action: Past, Present, and Future Applications},
year={2023},
url={https://openreview.net/forum?id=uU1eXPwesa}
}
```

## License

The datasets in this repository are released under the GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007). Please refer to the `LICENSE` file for detailed licensing information.



## Contact


If you have any questions, feedback, or inquiries about the code, feel free to reach out to the authors: [pablo.sanchez2@sony.com](mailto:pablo.sanchez2@sony.com) and [priyadarshini.kumari@sony.com](mailto:priyadarshini.kumari@sony.com).

If you encounter any issues with the datasets or have suggestions for improvements, please open an issue on this repository.


