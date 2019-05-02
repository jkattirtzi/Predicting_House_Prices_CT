## Predicting House Prices in Connecticut

Last year I was interested in selling our house in Connecticut. I had lots of questions. How much could we sell it for? When should we sell it. 

I decided to scrape some data. I found some nice tools on git hub. 

https://github.com/ChrisMuir/Zillow <br /> https://github.com/TheBecky/zillow-scraper

I made some small changes to these and include them in this repository. I then scrapped some data and started going through it. 

The notebook shows how I cleaned up the data to increase accuracy. 

I tried linear regression with regularization, random forest, Gradient Boosting. 

My accuracy was about 80%. This sounds good but is quite a high error when it comes to house prices. For example our $200,000 house was correct to +/- $40,000! 
There is a big difference between receiving $160,000 and $240,000! 

There is a lot more that can be done to increase accuracy. This was a fun little project. 
