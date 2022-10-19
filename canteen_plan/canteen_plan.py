import pandas as pd
import requests
import datetime
import config
from calendar import day_name


def get_daily_menu(offset: int) -> str:
    current_day = datetime.datetime.today().weekday()
    current_day += offset

    # Weekend -> Monday
    if current_day == 5 or current_day == 6:
        current_day = 0

    time_delta = datetime.timedelta(days=offset) + datetime.datetime.today()
    url = config.mensa_endpoint.replace("CURRENT_DATE",
                                        f"{time_delta.strftime('%Y')}%25252d{time_delta.strftime('%m')}%25252d{time_delta.strftime('%d')}")
    res = requests.get(url)
    df_plan = pd.read_html(res.text)[0]

    day_idx = (current_day % 7) * 2

    # check if day has data
    if df_plan.loc[day_idx].count() == 1:
        return "Die Mensa hat geschlossen!"

    pd.set_option('display.max_colwidth', None)
    df_day = df_plan.loc[day_idx]

    menu_string = ""

    for i in range(1, len(df_day)):
        menu_string += f"```{df_day.index[i]}: {df_day[i]}```"
            
    return menu_string


async def get_weekly_menu(ctx, weekly_offset: int) -> None:
    next_week = datetime.timedelta(weeks=weekly_offset) + datetime.datetime.today()
    next_monday = next_week - datetime.timedelta(days=next_week.weekday())
    offset = (next_monday - datetime.datetime.today()).days + 1

    await ctx.response.send_message(f"Der Essensplan für KW {next_week.isocalendar().week}:")
    
    for i in range(offset, offset + 5):
        print(i)
        print(get_daily_menu(i)[:50])
        await ctx.channel.send(f"**{day_name[i % offset]} ({(datetime.datetime.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y')}):**" + get_daily_menu(i))

    
