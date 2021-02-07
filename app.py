import os
from datetime import datetime, timedelta

from flask import Flask, request, render_template

app = Flask(__name__)


def make_date_from_str(date_string: str, template: str = "%Y-%m-%d") -> datetime:
    """
    Переводит дату из строки заданнаго формата в объект datetime.
    Можно указать только дату, и пользоваться дефорлтным шаблоном "%Y-%m-%d"
    """
    date_obj = datetime.strptime(date_string, template)

    return date_obj


def count_pregnacy_time(start_date: datetime, current_date: datetime = datetime.now()) -> timedelta:
    """
    Считает разницу между датами (объектами дат)
    """
    pregnacy_delta = current_date - start_date

    return pregnacy_delta


def data_to_weeks(pregnacy_delta: timedelta) -> str:
    weeks = pregnacy_delta.days // 7
    days = pregnacy_delta.days % 7

    result = f"{weeks} нед. {days} дн."

    return result


def period(str_date: str) -> str:
    start_date = make_date_from_str(str_date)

    delta = count_pregnacy_time(start_date)

    result = data_to_weeks(delta)

    return result


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/calc', methods=['GET', 'POST'])
def handle_data():
    mdt = request.form['MDT']
    udt = request.form['UDT']
    a = make_date_from_str(mdt)
    b = a + timedelta(weeks=40)
    c = period(mdt)
    d = datetime.date(b)
    e = d.year
    f = d.month
    g = d.day
    h = f'{g:02d}.{f:02d}.{e:02d}'
    i = make_date_from_str(udt)
    j = request.form['USN']
    k = request.form['USD']
    k1 = 7 * int(j)
    m = 280 - (int(k) + int(k1))
    n = i + timedelta(days=m)
    o = n.year
    p = n.month
    q = n.day
    r = f'{q:02d}.{p:02d}.{o:02d}'

    if int(j) == 0 and int(k) == 0:
        r = h
    else:
        pass

    if int(j) < 0 or int(k) < 0:
        r = h
    else:
        pass

    def_text = f'Акушерский срок составляет: {c} \nПредполагаемая дата родов: {h} \nДата родов по УЗИ: {r}'
    return render_template('index.html', def_text=def_text)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
