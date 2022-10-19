import pandas
import requests
import datetime

from settings import values



def get_daily_menu() -> str:
    current_day = datetime.datetime.today().weekday()
    if current_day == 5 or current_day == 6:
        current_day = 0

    url =  values.settings.mensa_endpoint.replace("CURRENT_DATE", datetime.datetime.today().strftime("%Y-%m-%d"))

    # https://www.stw-ma.de/Essen+_+Trinken/Speisepl%C3%A4ne/Mensaria+Metropol-date-2022%25252d10%25252d19-view-week.html

    res = requests.get(url)
    df_plan = pandas.read_html(res.text)[0]
    if df_plan.loc[current_day*2].count() == 1:
        return "Die Mensa hat geschlossen!"
    return df_plan.loc[current_day*2].to_string()

print(get_daily_menu())