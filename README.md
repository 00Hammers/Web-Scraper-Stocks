# Web-Scraper-Stocks

A web scraper I made some time ago to:
  - learn Python
  - learn how a web scraper worked
  - have an useful automation tool for checking stocks

The script reads a list of stocks from a text file, and looks up some data about them and save them in a CSV file.
It then performs a few simple checks on the returns, income and debt of the companies.
The stocks which pass these checks are saved in a second CSV file.

It's not an analysis tool, but more like a way to avoid wasting time with manual and ripetitive searching/writing activities.

Packages used:
  - selenium
  - bs4
