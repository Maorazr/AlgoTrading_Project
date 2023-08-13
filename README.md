
<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>AlgoTrading_Project
</h1>
<h3>◦ Unleash the Power of Algorithms!</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/.ENV-ECD53F.svg?style&logo=dotenv&logoColor=black" alt=".ENV" />
<img src="https://img.shields.io/badge/Gunicorn-499848.svg?style&logo=Gunicorn&logoColor=white" alt="Gunicorn" />
<img src="https://img.shields.io/badge/Plotly-3F4F75.svg?style&logo=Plotly&logoColor=white" alt="Plotly" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />

<img src="https://img.shields.io/badge/pandas-150458.svg?style&logo=pandas&logoColor=white" alt="pandas" />
<img src="https://img.shields.io/badge/NumPy-013243.svg?style&logo=NumPy&logoColor=white" alt="NumPy" />
<img src="https://img.shields.io/badge/Dash-008DE4.svg?style&logo=Dash&logoColor=white" alt="Dash" />
<img src="https://img.shields.io/badge/JSON-000000.svg?style&logo=JSON&logoColor=white" alt="JSON" />
</p>
<img src="https://img.shields.io/github/languages/top/Maorazr/AlgoTrading_Project?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/Maorazr/AlgoTrading_Project?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/Maorazr/AlgoTrading_Project?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/Maorazr/AlgoTrading_Project?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---


## 📍 Overview

The AlgoTrading_Project is a comprehensive codebase that provides a range of functionalities for algorithmic trading and financial analysis. It includes features such as a GUI application, data scraping and processing, strategy backtesting, statistical analysis, plotting of financial charts with indicators, and integration with AWS S3 for data storage. The project's purpose is to provide traders and financial analysts with a flexible and customizable platform to develop, execute, and evaluate trading strategies. Its value proposition lies in its modularity, extensive functionality, and ability to handle large amounts of financial data efficiently.

---

## ⚙️ Features

| Feature                | Description                           |
| ---------------------- | ------------------------------------- |
| **⚙️ Architecture**     | The codebase follows a modular architecture with separate modules for different functionalities such as GUI, data analysis, strategies, data scraping, and performance evaluation. The system uses a web application framework (Dash) for visualizing data and a GUI library (CustomTkinter) for creating user interfaces. |
| **📖 Documentation**   | The documentation is minimal but provides a brief overview of each file's purpose and functionality. However, it lacks extensive explanations or examples for using the different modules and features. |
| **🔗 Dependencies**    | The system relies on external libraries such as yfinance, pandas, boto3, Dash, Plotly, and CustomTkinter for various functionalities like retrieving financial data, data manipulation, AWS S3 interaction, data visualization, and GUI creation. |
| **🧩 Modularity**      | The system exhibits good modularity by separating different components into their respective files and modules. Each module serves a specific purpose, allowing for easy interchangeability and reusability. |
| **✔️ Testing**          | The codebase lacks extensive testing strategies and tools. Some of the code snippets contain unit tests using the `unittest.mock.patch` module. However, overall, there is room for improvement in terms of comprehensive testing coverage. |
| **⚡️ Performance**      | The performance of the system can vary depending on the data size and the complexity of the calculations being performed. Since the system involves data manipulation and analysis, it is crucial to optimize the algorithms and leverage efficient libraries like pandas to improve performance. |
| **🔐 Security**        | The codebase does not extensively address security measures. It relies on environment variables to store AWS credentials and bucket name, which is a good practice. However, other security aspects like input validation and authentication are not prominently addressed. Proper security measures should be implemented to protect user data and system functionality. |
| **🔀 Version Control** | The codebase is hosted on GitHub, utilizing Git for version control. It follows a centralized approach and lacks detailed commit messages and branches, making it challenging to track changes and collaborate effectively. Adopting proper branching strategies like GitFlow and providing descriptive commit messages would improve version control management. |
| **🔌 Integrations**    | The system integrates with external platforms like Yahoo Finance for data retrieval and with AWS S3 for storage and access of processed data. It leverages libraries like yfinance and boto3 to establish connections with these platforms. Enhancements can be made by integrating additional data providers and supporting different storage systems. |
| **📶 Scalability**     | The system's scalability depends on various factors like the efficiency of data processing algorithms, the ability to handle large datasets, and the responsiveness of the GUI components. It would benefit from optimizations and parallelization techniques to handle increasing data volumes and user interactions. |


---


## 📂 Project Structure


```bash
repo
├── Data
│   ├── OHLCV
│   ├── Processed
│   ├── Results
│   └── Summary
├── GUI
│   └── src
│       ├── actions
│       │   ├── __pycache__
│       │   │   └── download_OHLCV.cpython-311.pyc
│       │   └── download_OHLCV.py
│       ├── main.py
│       └── myApp.py
├── algo_app
│   ├── Procfile
│   ├── __pycache__
│   │   ├── _app.cpython-311.pyc
│   │   ├── app.cpython-311.pyc
│   │   ├── database.cpython-311.pyc
│   │   ├── getFiles.cpython-311.pyc
│   │   ├── origin_data.cpython-311.pyc
│   │   ├── plot_functions.cpython-311.pyc
│   │   ├── res_data.cpython-311.pyc
│   │   ├── stats_data.cpython-311.pyc
│   │   └── temp.cpython-311.pyc
│   ├── _app.py
│   ├── getFiles.py
│   ├── origin_data.py
│   ├── pages
│   │   ├── __pycache__
│   │   │   ├── compare.cpython-311.pyc
│   │   │   ├── original_data.cpython-311.pyc
│   │   │   ├── results.cpython-311.pyc
│   │   │   └── statistics.cpython-311.pyc
│   │   ├── original_data.py
│   │   ├── results.py
│   │   └── statistics.py
│   ├── requirements.txt
│   ├── res_data.py
│   └── temp.py
└── src
    ├── __pycache__
    │   ├── backtest.cpython-311.pyc
    │   ├── backtest.cpython-39.pyc
    │   ├── dataScapling.cpython-311.pyc
    │   ├── file_chooser.cpython-311.pyc
    │   ├── main.cpython-311.pyc
    │   ├── models.cpython-311.pyc
    │   ├── models.cpython-39.pyc
    │   ├── strategies.cpython-311.pyc
    │   ├── strategies.cpython-39.pyc
    │   ├── summary.cpython-311.pyc
    │   ├── summary.cpython-39.pyc
    │   ├── uploadData.cpython-311.pyc
    │   ├── utils.cpython-311.pyc
    │   └── utils.cpython-39.pyc
    ├── backtest.py
    ├── dataScapling.py
    ├── file_chooser.py
    ├── generateRaws.py
    ├── main.py
    ├── models.py
    ├── run_all.py
    ├── run_scripts.py
    ├── strategies.py
    ├── summary.py
    ├── updateData.py
    ├── uploadData.py
    └── utils.py

16 directories, 54 files
```

---

## 🧩 Modules

<details closed><summary>Src</summary>

| File                                                                                            | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---                                                                                             | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [myApp.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/GUI/src/myApp.py)           | The code snippet is a simple example of a GUI application built using CustomTkinter. It includes features such as buttons, progress bars, sliders, entry fields, option menus, switches, textboxes, segmented buttons, and tabviews. The code also demonstrates event handling and function execution based on user actions.                                                                                                                                                                                                                                                                                                                  |
| [main.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/GUI/src/main.py)             | The provided code creates a GUI application using tkinter. It includes a window, a label, a dropdown, a text field, and a button. Users can select a script from the dropdown, enter input in the text field, and click the button to run the selected script with the provided input.                                                                                                                                                                                                                                                                                                                                                        |
| [uploadData.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/uploadData.py)     | This code snippet uploads a DataFrame to an AWS S3 bucket. It uses the Boto library to establish a connection with S3, converts the DataFrame to a CSV file, and uploads it to a specific folder in the S3 bucket, displaying progress using tqdm.                                                                                                                                                                                                                                                                                                                                                                                            |
| [models.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/models.py)             | The code snippet defines:-Enumerations for order types and position sides-Classes for broker instructions, positions, and strategies-Specific strategies using Bollinger Bands with RSI and CCI indicators-An exception class for out of money situations.                                                                                                                                                                                                                                                                                                                                                                                    |
| [strategies.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/strategies.py)     | This code snippet includes three strategy classes: BollingerRSIStrategy, BollingerCCIStrategy, and BuyAndHold. Each strategy defines methods for entering and exiting positions based on specific criteria. These classes inherit from a base Strategy class and utilize data from a pandas DataFrame.                                                                                                                                                                                                                                                                                                                                        |
| [generateRaws.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/generateRaws.py) | This code snippet generates rows of strategy summaries for a given ticker. It filters and selects relevant strategy summaries based on the ticker and excludes empty summaries. It then organizes the data into rows with specific information such as strategy name, total return, Sharpe ratio, max drawdown, etc., which are stored in a list and returned.                                                                                                                                                                                                                                                                                |
| [file_chooser.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/file_chooser.py) | The provided code snippet contains functions to select files, load data from a directory, and validate user input. It includes functionalities such as displaying available files, validating input types, parsing input values, and loading data into a DataFrame using pandas.                                                                                                                                                                                                                                                                                                                                                              |
| [updateData.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/updateData.py)     | The code updates CSV files stored in an AWS S3 bucket. It reads each file, processes it by removing unnecessary columns and calculating average trade duration, and then overwrites the file in the S3 bucket. The code uses boto3 for S3 API interactions and pandas for data manipulation.                                                                                                                                                                                                                                                                                                                                                  |
| [summary.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/summary.py)           | This code snippet defines a class'Summary' that calculates various financial metrics for a given dataset. It calculates metrics such as total return, sharpe ratio, downside deviation, max drawdown, best/worst trade, number of trades, positive trades, and positive trading days. It then prints the results for each combination of ticker and strategy, and saves the summary statistics to a CSV file. It also offers the option to upload the CSV file to AWS S3.                                                                                                                                                                     |
| [utils.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/utils.py)               | This code snippet includes two functions. The first function, "adjust_types", takes a pandas DataFrame as input and adjusts the data types of various columns. The second function, "add_zero", takes a string representing a datetime and adds a "0" before the hour if needed.                                                                                                                                                                                                                                                                                                                                                              |
| [dataScapling.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/dataScapling.py) | The provided code snippet is a program that performs various calculations on financial data. It allows users to download OHLCV (Open, High, Low, Close, Volume) data for a list of ETFs from Yahoo Finance, calculates technical indicators such as Simple Moving Average (SMA), Standard Deviation (STD), Commodity Channel Index (CCI), and Relative Strength Index (RSI), and then saves the processed data to a file. Users can choose different parameters for the calculations and have the option to upload the processed data to an S3 bucket. The code is modular and well-structured, with separate functions for each calculation. |
| [run_scripts.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/run_scripts.py)   | The provided code snippet includes functions to run different scripts with specified parameters. It utilizes the `unittest.mock.patch` module to mock the input function and import the necessary script modules (`dataScalping`, `main`, and `summary`). The `run_scripts` function takes a list of parameter sets as input and sequentially runs the `run_dataScalping`, `run_main`, and `run_summary` functions for each parameter set. Overall, this code facilitates parameterized execution of multiple scripts.                                                                                                                        |
| [run_all.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/run_all.py)           | In this code snippet, there are three main functionalities being used. First, it calls the'dataScrapling' function from a module called'dataScrapling'. Then, it calls the'main' function from a module called'main'. Finally, it calls the'summary' function from a module called'summary'. All three functions are called sequentially in a'run_all' function, which is then executed when the code is run.                                                                                                                                                                                                                                 |
| [main.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/main.py)                 | This code snippet performs a backtest on financial data using various trading strategies and saves the results to a CSV file. It prompts the user for input parameters such as stop loss, RSI thresholds, and CCI thresholds. It then runs the backtest for each strategy on different tickers and combines the results into a single dataframe. The final dataframe is then saved to a CSV file and can be optionally uploaded to an S3 bucket.                                                                                                                                                                                              |
| [backtest.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/src/backtest.py)         | The provided code snippet is a backtesting framework that allows users to evaluate the performance of trading strategies. It accepts data, commission rates, initial balance, strategy parameters, and performs simulated trading based on the strategy's entry and exit signals. The output is a dataframe containing trading actions, positions, returns, and balances for further analysis.                                                                                                                                                                                                                                                |

</details>

<details closed><summary>Actions</summary>

| File                                                                                                            | Summary                                                                                                                                                                                                                                                                                                  |
| ---                                                                                                             | ---                                                                                                                                                                                                                                                                                                      |
| [download_OHLCV.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/GUI/src/actions/download_OHLCV.py) | This code snippet performs the following functionalities:1. Downloads historical financial data for a list of tickers within a specified date range from Yahoo Finance using the yfinance library.2. Validates user input for the ticker list and date range.3. Saves the downloaded data to a CSV file. |

</details>

<details closed><summary>Processed</summary>

| File                                                                                 | Summary                               |
| ---                                                                                  | ---                                   |
| [.csv](https://github.com/Maorazr/AlgoTrading_Project/blob/main/Data/Processed/.csv) | Prompt exceeds max token limit: 9628. |

</details>

<details closed><summary>Algo_app</summary>

| File                                                                                               | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ---                                                                                                | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| [_app.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/_app.py)               | This code snippet defines a Dash web application with multiple pages. It creates a navigation bar with links to each page and a page container where the content of each page is shown. The app runs in a debug mode when executed.                                                                                                                                                                                                                                          |
| [getFiles.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/getFiles.py)       | This code snippet provides functions to interact with an AWS S3 bucket. It supports listing files, retrieving files, reading files as CSV or JSON, and retrieving a default file based on its type (CSV or JSON). The code leverages the boto3 library and uses environment variables to store AWS credentials and bucket name.                                                                                                                                              |
| [temp.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/temp.py)               | This code snippet is a collection of functions and imports related to data visualization and analysis using the Dash and Plotly libraries. It includes functions to find and plot various indicators such as SMA, RSI, CCI, and Volume on a financial chart. Additionally, it provides functions to generate rows for strategy summaries and common traces for a given ticker symbol. The intent is to provide a comprehensive analysis and visualization of financial data. |
| [Procfile](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/Procfile)             | The provided code snippet runs a Python web application using the Gunicorn server. It starts the server using the "_app:server" as the entry point for the application.                                                                                                                                                                                                                                                                                                      |
| [origin_data.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/origin_data.py) | This code snippet imports necessary modules and defines a function'origin_data' that generates a Plotly graph with multiple traces representing ticker data. The layout and styling of the graph are also configured within the function. The resulting graph is returned as the output.                                                                                                                                                                                     |
| [res_data.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/res_data.py)       | The code snippet defines a function "res_data" that generates a plot using the Plotly library. The plot displays the close prices of a stock and various indicators (RSI, CCI, and Volume) based on the data provided. The function also customizes the layout of the plot and returns it.                                                                                                                                                                                   |

</details>

<details closed><summary>Pages</summary>

| File                                                                                                         | Summary                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                                          | ---                                                                                                                                                                                                                                                                                                                                                                                                              |
| [original_data.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/pages/original_data.py) | This code snippet is a part of a Dash web application that allows users to select a stock ticker from a dropdown menu. The selected stock's data is then plotted on a graph using the "origin_data" function. The graph is dynamically updated when the user chooses a different stock ticker. The layout consists of a dropdown menu and a graph.                                                               |
| [results.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/pages/results.py)             | The code snippet imports necessary modules and defines a Dash application layout. It sets up dropdown menus for selecting indicators, tickers, and a trading strategy. It also creates a graph to display stock data based on the selected inputs. The code calculates dtick, filters the data, and updates the graph based on the selected options.                                                             |
| [statistics.py](https://github.com/Maorazr/AlgoTrading_Project/blob/main/algo_app/pages/statistics.py)       | The provided code snippet imports the necessary modules and defines a web app layout using the Dash framework. It includes a dropdown menu to select a stock ticker and a graph to display statistical data for the selected stock. The app dynamically updates the graph based on the selected stock ticker. The code also includes functions to fetch and process the statistical data for the selected stock. |

</details>

---

## 🚀 Getting Started

### ✔️ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - `ℹ️ Requirement 1`
> - `ℹ️ Requirement 2`
> - `ℹ️ ...`

### 📦 Installation

1. Clone the AlgoTrading_Project repository:
```sh
git clone https://github.com/Maorazr/AlgoTrading_Project
```

2. Change to the project directory:
```sh
cd AlgoTrading_Project
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using AlgoTrading_Project

```sh
python main.py
```

### 🧪 Running Tests
```sh
pytest
```

---


## 🗺 Roadmap

> - [X] `ℹ️  Task 1: Implement X`
> - [ ] `ℹ️  Task 2: Refactor Y`
> - [ ] `ℹ️ ...`


---

## 🤝 Contributing

Contributions are always welcome! Please follow these steps:
1. Fork the project repository. This creates a copy of the project on your account that you can modify without affecting the original project.
2. Clone the forked repository to your local machine using a Git client like Git or GitHub Desktop.
3. Create a new branch with a descriptive name (e.g., `new-feature-branch` or `bugfix-issue-123`).
```sh
git checkout -b new-feature-branch
```
4. Make changes to the project's codebase.
5. Commit your changes to your local branch with a clear commit message that explains the changes you've made.
```sh
git commit -m 'Implemented new feature.'
```
6. Push your changes to your forked repository on GitHub using the following command
```sh
git push origin new-feature-branch
```
7. Create a new pull request to the original project repository. In the pull request, describe the changes you've made and why they're necessary.
The project maintainers will review your changes and provide feedback or merge them into the main branch.

---

## 📄 License

This project is licensed under the `ℹ️  INSERT-LICENSE-TYPE` License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional info.

---

## 👏 Acknowledgments

> - `ℹ️  List any resources, contributors, inspiration, etc.`

---
