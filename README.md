# Motivation
Mortgage interest rates went to all time lows (~2.7% 30 yr fixed) in 2020. At the same time, since the inception of the S&P 500 index, we've seen the index return ~11% per year. Therefore, you can withdraw cash from your home for ~2.7% and invest it to get a return of ~11% in the S&P 500 and pocket the difference.

The idea sounds good intuitively, but **what loan terms would give the optimal return and how much would we expect to make?** This script does the math with an assumption on index returns to help with decision making as you negotiate different loan estimates.

# What is this repo?
Just one script ``` mortgage_calculator.py``` which has a few useful methods in it:
1. ```calc_profit``` - Calculates the per year return of reinvesting a cashout refinance in indexes given a loan estimate
2. ```print_refinance_2020``` - Prints all the per year returns of all the loan estimates in the method to help with decision making
3. ```plot_heatmaps``` - Generates a plot of the projected returns for all interest rates and loan amounts (see plot below). Useful for getting a high level understanding of which combinations of interest rate, loan amount, and loan term result in more projected returns.

## Projected Profits Across Interest Rate & Loan Amount (Color = per year return in $$)
Some observations:
1. **15 year refinance returns strictly more than 30 year on a per year basis** -  Makes sense since the returns are similar at the beginning but get averaged over a smaller time period.
2. **Loan amount is a larger driver of returns than lower interest rate** - Makes sense since the small 10th of a percent changes in mortgage interest rate are relatively small compared to the % increase in principal if we borrow more money.
<img src=heatmaps.png>

# Usage
The loan estimates are hardcoded into the script. See ```print_refinance_2020``` and ```print_refinance_2021```. If you want to run some numbers you add some LoanEstimates to the script and run it and compare how much you'd anticipate to profit per year.

# Q&A
1. What if the S&P 500 returns less than the historical 11%? **Possible. If you want to be extra safe lower the assumed index returns to see if the returns are still positive.** Returns were still positive even when I lowered the assumed index returns to 7%. This gave me confidence to go through with this strategy.
2. From the plots, it seems like 15 year loans will result in strictly greater returns than 30 year. Why even consider 30 year? For me personally, 30 year was better for two reasons:
    1. **Minimize risk of lower than historical S&P 500 returns** - I figured that returns from the S&P500 would tend towards the historical average the more years I left my money in.
    2. **15 year loans require higher monthly payments** - I didn't want to exhaust all of the money coming from my salary to feed my refinances. 30 year loans allow me to have a more healthy amount of cashflow.
