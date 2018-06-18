import datetime


principle_paid_dict = {
    '2/1/2018': 400,
    '3/1/2018': 420
}

interest_paid_dict = {
    '2/1/2018': 20
}


def daily_reporting(**kwargs):
    principle = kwargs.get('principle', 1000)
    interest_rate = kwargs.get('interest_rate', 0.10)
    grace_period = kwargs.get('grace', 3)
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    loan_limit = kwargs.get('loan_limit', 3000)
    due_date = datetime.datetime.strptime(kwargs.get('due_date', '15/1/2018'), '%d/%m/%Y')
    actual_due_date = due_date + datetime.timedelta(days=grace_period)
    principle_paid_dict = kwargs.get('principle_paid_dict', {})
    interest_paid_dict = kwargs.get('interest_paid_dict', {})
    limit = kwargs.get('limit', 30)
    comp_period = kwargs.get('comp_period', 360)
    # initialize
    principle_paid = 0
    interest_paid = 0
    outstanding_principle = principle
    outstanding_interest = 0
    principle_overdue = 0
    interest_overdue = 0
    results = []
    # calculations
    for i in range(1, limit+1):
        date = start_date + datetime.timedelta(days=i)
        interest_amount = principle * (1 + (interest_rate/comp_period)) - principle

        for key, value in interest_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                interest_paid = value
        outstanding_interest = outstanding_interest - interest_paid + \
                               ((outstanding_principle * interest_rate * 1) / comp_period)

        for key, value in principle_paid_dict.items():
            if date == datetime.datetime.strptime(key, '%d/%m/%Y'):
                principle_paid = value
        outstanding_principle = principle + interest_amount - principle_paid

        principle_overdue = outstanding_principle - principle_paid if date > actual_due_date \
            else principle_overdue

        interest_overdue = outstanding_interest - interest_paid if date > actual_due_date \
            else interest_overdue

        results.append(
            {
                'id': i,
                'date': date.strftime('%d/%m/%Y'),
                'interest': interest_amount,
                'outstanding_principle': outstanding_principle,
                'outstanding_interest': outstanding_interest,
                'principle_overdue': principle_overdue,
                'interest_overdue': interest_overdue
            }
        )

    return results


activities = [
    {
        'date': '1/1/2018',
        'interest_paid': 0,
        'money_borrowed': 1000,
        'principle_paid': 2000,

    },
    {
        'date': '3/1/2018',
        'interest_paid': 0,
        'money_borrowed': 1000,
        'principle_paid': 0,
    },
    {
        'date': '5/1/2018',
        'money_borrowed': 0,
        'interest_paid': 100,
        'principle_paid': 1010,
    },
    {
        'date': '5/1/2018',
        'money_borrowed': 0,
        'principle_paid': 0,
        'interest_paid': 1000
    }
]


def transaction_reporting(**kwargs):
    principle = kwargs.get('principle', 10000)
    interest_rate = kwargs.get('interest_rate', 5/100)
    comp_period = kwargs.get('comp_period', 365)
    start_date = datetime.datetime.strptime(kwargs.get('start_date', '1/1/2018'), '%d/%m/%Y')
    activities = kwargs.get('activities', [])
    results = []

    outstanding_principle = principle
    outstanding_interest = 0
    for activity in activities:
        date = datetime.datetime.strptime(activity.get('date'), '%d/%m/%Y')
        interest_paid = activity.get('interest_paid')
        principle_paid = activity.get('principle_paid')
        money_borrowed = activity.get('money_borrowed')

        date_diff = date - start_date
        days = date_diff.days
        outstanding_interest = (outstanding_interest - interest_paid) + \
                               ((outstanding_principle*interest_rate*days) / comp_period)

        outstanding_principle = outstanding_principle - principle_paid + money_borrowed
        results.append({
            'date': date.strftime('%d/%m/%Y'),
            'interest_rate': interest_rate,
            'interest_paid': interest_paid,
            'principle_paid': principle_paid,
            'money_borrowed':  money_borrowed,
            'outstanding_interest': outstanding_interest,
            'outstanding_principle': outstanding_principle
        })

    return results









