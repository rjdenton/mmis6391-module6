from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

loan_amortization_detail = Blueprint('loan_amortization_detail', __name__)

@loan_amortization_detail.route('/loan_detail/<int:loan_info_id>')
def loan_detail(loan_info_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch the loan details using the loan_info_id
    cursor.execute('SELECT loan_amount, interest_rate, term_years FROM loan_info WHERE loan_info_id = %s', (loan_info_id,))
    loan_data = cursor.fetchone()

    # print(loan_data)

    # Convert the fetched data to the appropriate types
    loan_amount = float(loan_data['loan_amount'])  # Convert loan_amount from Decimal to float
    interest_rate = float(loan_data['interest_rate'])  # Convert interest_rate from Decimal to float
    loan_term_years = int(loan_data['term_years'])  # Convert loan_term_years to int

    # Create a function that calculates the loan amortization details
    def loan_amortization(loan_amount, interest_rate, loan_term_years):
        loan_term_months = loan_term_years * 12  # Convert loan term to months
        monthly_interest_rate = interest_rate / 12 / 100  # Calculate monthly interest rate

        # Calculate the monthly payment
        if monthly_interest_rate > 0:
            monthly_payment = loan_amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_term_months))
        else:
            monthly_payment = loan_amount / loan_term_months  # Handle no interest case

        # Create a list to store the loan amortization details
        loan_amortization_list = []

        # Loop to calculate the loan amortization details for each month
        for i in range(1, loan_term_months + 1):
            interest_paid = loan_amount * monthly_interest_rate  # Calculate interest paid for the current month
            principal_paid = monthly_payment - interest_paid  # Calculate principal paid
            remaining_balance = loan_amount - principal_paid  # Calculate remaining balance after payment

            # Append the details for the current month
            loan_amortization_list.append({
                'month': i,
                'starting_balance': loan_amount,
                'interest_paid': interest_paid,
                'principal_paid': principal_paid,
                'monthly_payment': monthly_payment,
                'remaining_balance': remaining_balance
            })

            # Update the loan amount for the next month
            loan_amount = remaining_balance

        return loan_amortization_list

    # Get the amortization details
    amortization_schedule = loan_amortization(loan_amount, interest_rate, loan_term_years)

    # Render the loan detail template and pass the amortization schedule
    return render_template('loan_detail.html', loan_schedule=amortization_schedule, loan_id=loan_info_id)