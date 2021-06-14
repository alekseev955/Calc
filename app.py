import os
from datetime import datetime, timedelta
from flask import Flask, request, render_template

app = Flask(__name__)

## \brief Функция перевода даты из str в datetime-объект
## \details При чтении HTML-формы приложения получаем дату в str-формате
## \details Её необходимо перевести в читаемый формат datetime для последующей машинной обработки
## \param date_string дата в строчном формате
## \param template шаблон входных данных
## \return объект даты


def make_date_from_str(date_string: str, template: str = "%Y-%m-%d") -> datetime:

    date_obj = datetime.strptime(date_string, template)

    return date_obj

## \brief Функция для расчёта срока беременности
## \param start_date прочитанная с HTML-формы дата
## \param current_date текущая дата
## \return результат расчёта дельты


def count_pregnacy_time(start_date: datetime, current_date: datetime = datetime.now()) -> timedelta:

    pregnacy_delta = current_date - start_date

    return pregnacy_delta

## \brief Функция для перевода срока беременности в формат недели/дни
## \param pregnacy_delta рассчитанный срок
## \return результат в днях и неделях


def data_to_weeks(pregnacy_delta: timedelta) -> str:
    weeks = pregnacy_delta.days // 7
    days = pregnacy_delta.days % 7

    result = f"{weeks} нед. {days} дн."

    return result

## \brief Функция для вывода даты в неделях
## \param str_date дата в str-представлении
## \return результат в неделях


def period(str_date: str) -> str:
    start_date = make_date_from_str(str_date)

    delta = count_pregnacy_time(start_date)

    result = data_to_weeks(delta)

    return result


@app.route('/', methods=['GET', 'POST'])
## \brief Функция для генерации index.html
## \return HTML-страница
def index():
    return render_template('index.html')


@app.route('/calc', methods=['GET', 'POST'])
## \brief Расчёт параметров, рендер HTML-шаблона
## \return HTML-страница с результатом вычислений
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
