import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass


@dataclass
class LoanEstimate:
    company_name: str
    loan_amt: int
    interest_rate: float
    loan_term: int
    fixed_cost: float


def calc_profit(
    loan_amt: int,
    interest_rate: float,
    loan_term: int,
    fixed_cost: float,
    index_returns: float = 0.11,
):
    """Returns the projected profit per year from a cashout refinance invested
    into index funds based off historical index returns"""
    working_principle = loan_amt
    aggregate = 0
    r = interest_rate / 12
    n = loan_term * 12
    """
    M = P[r(1+r)^n/((1+r)^n)-1)] = the total monthly mortgage payment.
    P = the principal loan amount.
    r = your monthly interest rate.
    n = number of payments over the loan’s lifetime.
    """
    monthly_payment = loan_amt * ((r * ((1 + r) ** n)) / (((1 + r) ** n) - 1))

    # for every monthly payment
    for _ in range(n):
        # amt made in stocks this month
        aggregate += working_principle * (index_returns / 12)

        interest_payment = working_principle * r
        # amt paid in interest this month
        aggregate -= interest_payment
        # amt paid in principle this month
        working_principle -= monthly_payment - interest_payment

    # remove fixed costs less the opportunity cost of index returns
    aggregate -= fixed_cost * (1 + index_returns) ** loan_term
    return aggregate / loan_term


def generate_profits(
    loan_amt_min: int,
    loan_amt_max: int,
    interest_rate_min: float,
    interest_rate_max: float,
    loan_term: int,
):
    """generates a 2D array of all the projected profits
    for all interest rates and loan amt pairs using the passed in
    loan term"""
    # convert to int so we can generate ranges easily
    interest_int_min = int(interest_rate_min * 10000)
    interest_int_max = int(interest_rate_max * 10000)

    coords = []
    interest_step = 10
    # for all potential interest rates
    for interest_int in range(interest_int_min, interest_int_max, interest_step):
        col = []
        # for all potential loan amts
        for loan_amt in range(loan_amt_min, loan_amt_max, 20000):
            interest_rate = interest_int / 10000

            col.append(
                calc_profit(
                    loan_amt=loan_amt,
                    interest_rate=interest_rate,
                    loan_term=loan_term,
                    fixed_cost=0,
                )
                / loan_term
            )

        coords.append(col)

    return np.array(coords)


def plot_heatmaps():
    """plots projected profits across reasonable ranges of interest rate
    and loan amount per year for a 15/30 yr term for visualization of
    all profit pairs"""
    min_loan = 300000
    max_loan = 1000000
    min_interest = 0.029
    max_interest = 0.04
    xtick_ints = range(min_loan, max_loan, 20000)
    xticklabels = [f"${num}" for num in xtick_ints]
    ytick_ints = range(int(min_interest * 10000), int(max_interest * 10000), 10)
    yticklabels = [f"{num/100}%" for num in ytick_ints]
    loan_15_data = generate_profits(
        min_loan, max_loan, min_interest, max_interest, loan_term=15
    )
    loan_30_data = generate_profits(
        min_loan, max_loan, min_interest, max_interest, loan_term=30
    )
    fig, axes = plt.subplots(nrows=2, figsize=(12, 12))
    ax1, ax2 = axes

    vmax = max(np.amax(loan_15_data), np.amax(loan_30_data))
    vmin = min(np.amin(loan_15_data), np.amin(loan_30_data))

    # Heat maps.
    im1 = ax1.matshow(loan_15_data, vmin=vmin, vmax=vmax, cmap="coolwarm")
    im2 = ax2.matshow(loan_30_data, vmin=vmin, vmax=vmax, cmap="coolwarm")

    # Formatting for heat map 1.
    ax1.set_xticks(range(len(xticklabels)))
    ax1.set_yticks(range(len(yticklabels)))
    ax1.set_xticklabels(xticklabels)
    ax1.set_yticklabels(yticklabels)
    ax1.set_title("15 Year Loan", y=-0.1)
    plt.setp(ax1.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
    plt.colorbar(im1, fraction=0.045, pad=0.05, ax=ax1)

    # Formatting for heat map 2.
    ax2.set_xticks(range(len(xticklabels)))
    ax2.set_yticks(range(len(yticklabels)))
    ax2.set_xticklabels(xticklabels)
    ax2.set_yticklabels(yticklabels)
    ax2.set_title("30 Year Loan", y=-0.1)
    plt.setp(ax2.get_xticklabels(), rotation=45, ha="left", rotation_mode="anchor")
    plt.colorbar(im2, fraction=0.045, pad=0.05, ax=ax2)

    fig.tight_layout()
    plt.show()


def print_formated_profit(estimate: LoanEstimate) -> None:
    profit = calc_profit(
        loan_amt=estimate.loan_amt,
        interest_rate=estimate.interest_rate,
        loan_term=estimate.loan_term,
        fixed_cost=estimate.fixed_cost,
    )
    print(f"{estimate.company_name} {estimate.loan_term} year: ${profit:.2f}")


def print_refinance_2020() -> None:
    """These are real rates I obtained during negotiations with loan estimates in 2020.
    It was a cashout refi, credit score was >760 at the time if I recall correctly."""

    estimates = [
        LoanEstimate(
            company_name="Aimloan",
            loan_amt=500000,
            interest_rate=0.03625,
            loan_term=30,
            fixed_cost=1037.50,
        ),
        LoanEstimate(
            company_name="Aimloan",
            loan_amt=500000,
            interest_rate=0.0375,
            loan_term=30,
            fixed_cost=0,
        ),
        LoanEstimate(
            company_name="Sebonic",
            loan_amt=500000,
            interest_rate=0.0349,
            loan_term=30,
            fixed_cost=3040,
        ),
        LoanEstimate(
            company_name="Sebonic",
            loan_amt=500000,
            interest_rate=0.03615,
            loan_term=30,
            fixed_cost=856,
        ),
        LoanEstimate(
            company_name="Quicken",
            loan_amt=515000,
            interest_rate=0.0375,
            loan_term=30,
            fixed_cost=1131,
        ),
        LoanEstimate(
            company_name="Quicken",
            loan_amt=515000,
            interest_rate=0.0375,
            loan_term=30,
            fixed_cost=-995.55,
        ),
    ]

    for estimate in estimates:
        print_formated_profit(estimate)


def print_refinance_2021():
    """These are real rates I obtained during negotiations with loan estimates in 2021.
    It was a cashout refi, credit score was ~768 at the time."""

    estimates = []

    for estimate in estimates:
        print_formated_profit(estimate)


if __name__ == "__main__":
    # simple test suite
    all_tests_passed = True
    all_tests_passed &= (
        calc_profit(loan_amt=510000, interest_rate=0.03125, loan_term=15, fixed_cost=0)
        - 160564
        < 1
    )
    if all_tests_passed:
        print("All tests passed!")

    # plot_heatmaps()
    # print_refinance_2020()
    print_refinance_2021()
