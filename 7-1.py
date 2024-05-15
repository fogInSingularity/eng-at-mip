# подключение нужных пакетов
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
import time
import numpy as np
from scipy.interpolate import make_interp_spline

GPIO.setwarnings(False)

# пины нужных портов
comp = 14
dac = [8, 11, 7, 1, 0, 5, 12, 6]
led = [2, 3, 4, 17, 27, 22, 10, 9]
troyka = 13

# установка в мод BCM
GPIO.setmode(GPIO.BCM)

# настрокайка пинов на ввод-вывод
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp, GPIO.IN)

# функция перевода из 10 записи в 2 запись
def num_to_bin(num):
    return [int(i) for i in bin(num)[2:].zfill(8)]

# функция получения adc
def adc():
    num = 0
    for i in range(7, -1, -1):
        num += 2**i
        GPIO.output(dac, num_to_bin(num))
        time.sleep(0.005)
        comp_val = GPIO.input(comp)
        if (comp_val == 1):
            num -= 2**i
    return num

# функция вывода на dac напряжения и возвращение его предмтавлния в 2 сс строкой
def comp_to_disco(num):
    str = num_to_bin(num)
    GPIO.output(dac, str)
    return str

# список измерений вольт
data_volts = []

val = 0

# тройка = high
GPIO.output(troyka, 1)
# начальное время
time_start = time.time()

# зарядка
print("Зарядка")
while(val < 206):
    val = adc()
    print(val)
    comp_to_disco(val)
    data_volts.append(val)

# тройка = low
GPIO.output(troyka, 0)

# разрядка
print("Разрядка")
while (val > 170):
    print(val)
    val = adc()
    comp_to_disco(val)
    data_volts.append(val)

# конечное время
time_end = time.time()

# массив времени
data_times = []
for i in range(0, len(data_volts)):
    t = (time_end - time_start)/len(data_volts)
    data_times.append(i * t)

# записать измерения вольт
data_volts_str = [str(i) for i in data_volts]
with open("data.txt", "w") as file:
    file.write("\n".join(data_volts_str))

# записать в settings.txt среднее время и деление
with open("settings.txt", "w") as file:
    file.write(str((time_end - time_start)/len(data_volts)))
    file.write("\n")
    file.write(str(3.3/256))

# показать график

xy_spline = make_interp_spline(data_times, data_volts)
x = np.linspace(min(data_times), max(data_times), 70)
y = xy_spline(x)

plt.plot(x, y)
plt.show()

# plt.plot(data_times, data_volts)
# plt.show()