import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
pd.options.mode.chained_assignment = None

# Таблица DataFrame
df = pd.DataFrame(
    {
        "Год/Месяц": ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
        "2017": [65000, 61000, 63000, 0, 70580, 97365, 104755, 101820, 83655, 77910, 70365, 64200],
        "2018": [69550, 65270, 67410, 73830, 75521, 0, 112088, 108947, 89511, 83364, 75291, 68694],
        "2019": [71358, 66967, 69163, 75750, 77484, 106889, 115002, 111780, 91838, 85531, 0, 70480],
        "2020": [77781, 0, 75387, 82567, 84458, 116509, 125352, 0, 100104, 93229, 84200, 76823],
        "2021": [81670, 76644, 79157, 86695, 88681, 122335, 131620, 127932, 105109, 97890, 88410, 80664],
        "2022": [89837, 84308, 87072, 95365, 97549, 134568, 144782, 140725, 115620, 107679, 97252, 88731],
     }
)

year = 2017
a = 0
i = 0
b = 1
avg = 0

#заполнение пустых месяцев
for i in range(5):
    for a in range(12):
        if df[str(year)].loc[df.index[a]] == 0:
            apr = df[str(year)].loc[df.index[a - 1]] * (df[str(year + 1)].loc[df.index[a]] / df[str(year + 1)].loc[df.index[a - 1]])
            apr = round(apr)
            df[str(year)].iloc[df.index[a]] = apr
    year += 1

a = 6
#среднее
for i in range(13):
    if i == 12:
        break
    avg = avg + df.iloc[i, a]
avg = avg / i
avg = round(avg, 2)
sum = avg * i
list = []
x = 0
for i in range(-10, 2, 1):
    b = x * df.iloc[i, a]
    if b > 0:
        b = -b
    list.append(b)
    x += 1
    i += 1
c = np.sum(list)


i = 12
#b для линейного тренда
lT_b = (i * c - sum * (-66)) / (i * 506 - 4356)
lT_b = round(lT_b, 6)
lT = (sum-lT_b * (-66))/12
lT = round(lT)

#а для линейного тренда
lT_a = lT-lT_b*12
lT_a = round(lT_a, 5)


period = i + 1
i = 0
g = 0
k = 0
while g < 2:
    df.insert(a+1, str(year + 1), '',)  # создаём новый год в списке
    while k < 12:
        trend = lT_b*period+lT_a
        trend = round(trend)  # тренд
        index = df.iloc[i, 6]/avg
        index = round(index, 2)  # индекс
        prognoz = trend * index
        prognoz = round(prognoz)  # прогноз
        df.iloc[i, a + 1] = prognoz  # присваиваем найденное значение ячейке таблицы
        i += 1
        period += 1
        k += 1
    g += 1
    k = 0
    i = 0
    year += 1
    a += 1
#23
df.insert(a+1, str('razn'), '')
for i in range(12):
    df['razn'].loc[df.index[i]] = df[str(year - 1)].loc[df.index[i]] - avg

df.insert(a+2, str('razn**2'), '')
for i in range(12):
    df['razn**2'].loc[df.index[i]] = df['razn'].loc[df.index[i]] ** 2
total = df['razn**2'].sum()
r_total = round(total)
r_total = r_total / 12
r_total = r_total ** 0.3085
r_total = round(r_total) #srednee otklonenie

df.insert(a+3, str('optimist23'), '')
for i in range(12):
    df['optimist23'].loc[df.index[i]] = df[str(year - 1)].loc[df.index[i]] + r_total

df.insert(a+4, str('pissimist23'), '')
for i in range(12):
    df['pissimist23'].loc[df.index[i]] = df[str(year - 1)].loc[df.index[i]] - r_total

#24
df.insert(a+5, str('razn x2'), '')
for i in range(12):
    df['razn x2'].loc[df.index[i]] = df[str(year )].loc[df.index[i]] - avg

df.insert(a+6, str('razn**2 x2'), '')
for i in range(12):
    df['razn**2 x2'].loc[df.index[i]] = df['razn x2'].loc[df.index[i]] ** 2
total2 = df['razn**2 x2'].sum()
r_total2 = round(total2)
r_total2 = r_total2 / 12
r_total2 = r_total2 ** 0.3085
r_total2 = round(r_total2) #srednee otklonenie

df.insert(a+7, str('optimist24'), '')
for i in range(12):
    df['optimist24'].loc[df.index[i]] = df[str(year )].loc[df.index[i]] + r_total2

df.insert(a+8, str('pissimist24'), '')
for i in range(12):
    df['pissimist24'].loc[df.index[i]] = df[str(year)].loc[df.index[i]] - r_total2
df.drop(columns=['razn x2', 'razn**2 x2', 'razn**2', 'razn'], inplace=True)


# Сброс ограничений на количество выводимых рядов
pd.set_option('display.max_rows', None)
# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)


fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
plt.plot(df['2023'], label='Прибыль за год')
plt.plot(df['optimist23'], label='Позитивный прогноз')
plt.plot(df['pissimist23'], label='Писсимистический прогноз')
ax.set_xlabel('Месяца')
ax.set_ylabel('Прибыль')
ax.set_title('2023')
ax.legend();

fig, ax = plt.subplots(figsize=(10, 7), layout='constrained')
plt.plot(df['2024'], label='Прибыль за год')
plt.plot(df['optimist24'], label='Позитивный прогноз')
plt.plot(df['pissimist24'], label='Писсимистический прогноз')
ax.set_xlabel('Месяца')
ax.set_ylabel('Прибыль')
ax.set_title('2024')
ax.legend();

plt.show()
print(df)
