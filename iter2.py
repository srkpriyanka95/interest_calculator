import requests
from bs4 import BeautifulSoup
import streamlit as st
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta



def rate_table_creation():

    # Define the URL of the website
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
    url = 'https://www.goodreturns.in/gold-rates/dindigul.html'

    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', cellpadding='1', cellspacing='1', width='100%')
        
        if table:
            title_ = table.find_all('tr')[0]
            title = [cell.get_text(strip=True) for cell in title_.find_all('td')]
            rate_table = pd.DataFrame(columns=title)
            gold_rate={}
            num=0
            for cell in table.find_all('tr')[1].find_all('td'):
                gold_rate[title[num]] = cell.get_text(strip=True)
                num+=1
            rate_table.loc[0]= gold_rate

            return rate_table


def date_difference_interest_calculation(amount,entered_date):
    today_date = datetime.date.today().strftime("%d-%m-%Y")
    try:
        initial_date = datetime.datetime.strptime(entered_date, "%d/%m/%y").date()
    except:
        initial_date = datetime.datetime.strptime(entered_date, "%d/%m/%Y").date()
    date_difference = relativedelta(datetime.date.today(),initial_date)
    year_diff = date_difference.years
    month_diff = date_difference.months
    day_diff = date_difference.days
    diff = f'{year_diff} years - {month_diff} months - {day_diff} days'
    if day_diff != 0:
        month_diff_ = month_diff+1
        total_months = (year_diff*12) + date_difference.months+1 
    else:
        total_months = (year_diff*12) + date_difference.months
    interest_per_month = amount*0.02
    net_interest = interest_per_month * total_months
    print(round(net_interest),round(amount+net_interest))
    total_interest = 0
    amount_with_interest = amount

    for i in range(1,(year_diff+1)):
        total_interest += interest_per_month * 12
        amount_with_interest = amount_with_interest + (interest_per_month * 12)
        interest_per_month = amount_with_interest*0.02
    total_interest += ((amount_with_interest * 0.02) * month_diff_)
    total_amount_with_interest = amount_with_interest + ((amount_with_interest * 0.02) * month_diff_)
    st.subheader(f':red[{diff}]')
    st.subheader('கடன் தொகை:')
    st.subheader(amount)
    st.subheader('மொத்த மாதங்கள்:')
    st.subheader(f':green[{total_months} Months]')
    st.subheader('மாத வட்டி:')
    st.subheader(round(amount*0.02))
    st.divider()
    st.subheader(':blue[Net வட்டி]')
    st.subheader('வட்டி:')
    st.subheader(f':red[{round(net_interest)}]')
    st.subheader("மொத்தம்:")
    st.subheader(f':green[{round(amount+net_interest)}]')
    st.divider()
    st.subheader(':blue[கூட்டு வட்டி]')
    st.subheader('வட்டி:')
    st.subheader(f':red[{round(total_interest)}]')
    st.subheader("மொத்தம்:")
    st.subheader(f':green[{round(total_amount_with_interest)}]')


st.title('Interest Calculator')
st.divider()
rate_table = rate_table_creation()
st.subheader('Gold Rate Today')
st.dataframe(rate_table,hide_index=True)
st.divider()
st.subheader("இன்றைய தேதி:")
st.subheader(datetime.date.today().strftime("%d-%m-%Y"))
st.subheader('தொகை:')
amount = st.text_input("","",key='amount')
try:
    amount = int(amount)
except:
    st.error('Please Enter a Number')
st.subheader('')
st.subheader('அடகு வைத்த தேதி:')
entered_date = st.text_input("","",key='date')
st.divider()
if amount and entered_date:
    date_difference_interest_calculation(amount,entered_date)



