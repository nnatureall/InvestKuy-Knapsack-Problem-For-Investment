# InvestKuy: Optimal Investment Recommendation System

InvestKuy is a smart solution designed to optimize your investment decisions using the Knapsack Problem approach. The app provides tailored investment recommendations based on your risk profile and investment duration.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Algorithms](#algorithms)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Risk Profile Selection**: Choose between Conservative, Moderate, or Aggressive risk profiles.
- **Investment Duration**: Short, Mid, or Long-term options available.
- **Algorithm Selection**: Supports multiple algorithms for investment optimization:
  - 0/1 Knapsack with Dynamic Programming
  - 0/1 Knapsack with Brute Force
  - 0/1 Knapsack with Greedy
  - Unbounded Knapsack with Dynamic Programming
  - Unbounded Knapsack with Greedy
- **User-Friendly Interface**: Built with Streamlit for a seamless user experience.

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/investkuy.git
    ```
2. Navigate to the project directory:
    ```bash
    cd investkuy
    ```
3. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
2. Open the app in your browser at `http://localhost:8501`.
3. Follow the on-screen instructions to:
    - Select your risk profile.
    - Choose your investment duration.
    - Set your initial investment capital.
    - Get optimized investment recommendations.

## Dataset

The app uses a dataset containing mutual fund information, including:
- Fund names
- Prices per lot
- Risk levels (low, medium, high)
- Historical returns over different durations (1M, 1Y, 3Y)

The dataset should be placed in the root directory and named `Invest Kuy_Clean Dataset - Investkuy_Dataset - Mutual_Funds.csv`.

## Algorithms

InvestKuy implements the following algorithms to solve the Knapsack Problem:

- **0/1 Knapsack**:
  - Brute Force: Examines all possible subsets to find the optimal solution.
  - Dynamic Programming: Uses a table to optimize the selection process.
  - Greedy: Selects items based on the highest value-to-weight ratio.

- **Unbounded Knapsack**:
  - Dynamic Programming: Optimizes for unlimited quantities of each item.
  - Greedy: Selects as many of the highest ratio items as possible.

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Make your changes and commit them:
    ```bash
    git commit -m "Add new feature"
    ```
4. Push your changes:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Happy Investing!** 🚀

