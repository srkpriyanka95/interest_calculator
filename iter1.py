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
    col1,col2,col3 = st.columns([1,3,1])
    col2.subheader(f':red[{diff}]')
    col1,col2,col3 = st.columns([3,0.5,3])
    col1.subheader('கடன் தொகை')
    col2.subheader(":")
    col3.subheader(amount)
    col1.subheader('மொத்த மாதங்கள்')
    col2.subheader(":")
    col3.subheader(f':green[{total_months} Months]')
    col1.subheader('மாத வட்டி')
    col2.subheader(":")
    col3.subheader(round(amount*0.02))
    st.divider()
    col1_,col2_,col3_ = st.columns([2,3,2])
    col2_.subheader(':blue[Net வட்டி]')
    col1,col2,col3= st.columns([3,0.5,3])
    col1.subheader('வட்டி')
    col2.subheader(":")
    col3.subheader(f':red[{round(net_interest)}]')
    col1.subheader("மொத்தம்")
    col2.subheader(":")
    col3.subheader(f':green[{round(amount+net_interest)}]')
    st.divider()
    col1_,col2_,col3_ = st.columns([2,3,2])
    col2_.subheader(':blue[கூட்டு வட்டி]')
    col1,col2,col3= st.columns([3,0.5,3])
    col1.subheader('வட்டி')
    col2.subheader(":")
    col3.subheader(f':red[{round(total_interest)}]')
    col1.subheader("மொத்தம்")
    col2.subheader(":")
    col3.subheader(f':green[{round(total_amount_with_interest)}]')


col1_,col2_,col3_ = st.columns([1,3,1])
col2_.title('Interest Calculator')
st.divider()
rate_table = rate_table_creation()
col1,col2,col3 = st.columns([1,3,1])
col2.markdown('<h3 style="text-align: center;">Gold Rate Today</h3>', unsafe_allow_html=True)
col2.dataframe(rate_table,hide_index=True)
st.divider()
col1,col2,col3 = st.columns([3,0.5,3])
col1.subheader("இன்றைய தேதி")
col2.subheader(':')
col3.subheader(datetime.date.today().strftime("%d-%m-%Y"))
col1.subheader('')
col1.subheader('தொகை')
col2.subheader('')
col2.subheader(':')
amount = col3.text_input("","",key='amount')
try:
    amount = int(amount)
except:
    st.error('Please Enter a Number')
col1,col2,col3 = st.columns([3,0.5,3])
col1.subheader('')
col1.subheader('அடகு வைத்த தேதி')
col2.subheader('')
col2.subheader(':')
entered_date = col3.text_input("","",key='date')
st.divider()
if amount and entered_date:
    date_difference_interest_calculation(amount,entered_date)



