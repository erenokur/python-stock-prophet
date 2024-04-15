## Python-Stock-Prophet

this project is under construction, the main goal is to predict the stock price using the Prophet library from Facebook.

## Description

This is a simple stock prediction program that uses the Prophet library to predict the future price of a stock. The program uses the yfinance library to download historical stock data and the Prophet library to predict future stock prices. The program then plots the historical stock data and the predicted future stock prices.

## Installation

```
pip install -r requirements.txt
```

**Note:** It's recommended to update all packages to ensure compatibility by using the following command:

```
pip install --upgrade --force-reinstall -r requirements.txt
```

For migrations:

```bash
flask db init
flask db migrate
flask db upgrade
```

you also need to create a `.env` file with the following variables:

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
EXTERNAL_API_KEY=your-api-key
```

## Future Work

1. **User Authentication:** Implement user authentication to secure user data and interactions.
2. **User Portfolio Page:** Create a user-friendly portfolio page for users to manage their stocks.
3. **User Portfolio Stock Prediction:** Enable users to predict the future prices of stocks in their portfolio.
4. **User Portfolio Stock Price Change Mail Notification:** Notify users via email about changes in the prices of stocks in their portfolio.
5. **Advanced Stock Analysis:** Utilize additional techniques such as LSTM, ARIMA, etc., to enhance stock price predictions.
6. **Financial Statement Analysis:** Incorporate balance sheet, income statement, and cash flow statement data for more accurate predictions.
7. **News Data Analysis:** Integrate news data analysis for better understanding of stock price movements.
8. **Social Media Data Analysis:** Analyze social media data to gauge sentiment and its impact on stock prices.
9. **Sentiment Analysis:** Perform sentiment analysis on news articles and social media data to predict stock price trends.
10. **Front-End Development:** Develop a user-friendly front-end interface for users to interact with the program seamlessly.
