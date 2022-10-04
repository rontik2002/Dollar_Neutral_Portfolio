# Dollar Neutral Portfolio (Low Market Risk) Algorithm
- Created an algorithm to produce a Dollar Neutral Portfolio using Beta, Stock Price (1 Yr) and Price to Book ratio.
- A Dollar Nuetral Portfolio is a portfolio management concept, in which there is equal investment in long and short positions based on price volatility of a security.
- According to “The Street View - How Design Choices Impact Low Factor Risk Performance” by TwoSigma, the Dollar Nuetral Portfolio would outperform all other       portfolios in a situation similar to that of the March 2020 stock market crash.
- Scraped data for all stocks in the S&P 500 using Python and Selenium.
- Graphed the distribution of beta and price to book ratio to identify Gaussian distribution and derive the individual z-scores for each security.
- Used pandas to weigh the z-scores to create a list of 18 stocks, each differently weighted, and equal investments in Long and Short positions.
