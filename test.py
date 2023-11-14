from main import main_

vse_norm = True
risk__, hor__, time__ = 0, 0, 0
k_risk = 0
k_hor = 0
fin = 1

a = int(input("Введите: "
              "\n 1 - если вы готовы тратить несколько часов в месяц на инвестиции "
              "\n 2 - если вы готовы тратить несколько часов в неделю на инвестиции "
              "\n 3 - если вы готовы тратить несколько часов в день на инвестиции\n"))
if a == 1:
    time__ = 7
elif a == 2:
    time__ = 17
elif a == 3:
    time__ = 30
else:
    vse_norm = False
    print("Ошибка, вы ввели некорректное значение")
if vse_norm:
    b = int(input("Введите на какой срок вы готовы сделать вложение (от 0 до 7)"
                  "\nгде 0 - это меньше года, а 7 - это больше 6 лет\n"))
    if 0 <= b <= 7:
        hor__ = b
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")

if vse_norm:
    c = int(input("Какие ваши ожидания от доходности? Введите 1, 2 или 3, где"
                  "\n 1 - Меньше или равна вкладу, не готов на риск"
                  "\n 2 - Немного выше вклада, готов на небольшой риск"
                  "\n 3 - Существенно выше вклада, готов на риск\n"))
    if c == 1:
        risk__ = 10
    elif c == 2:
        risk__ = 30
    elif c == 3:
        risk__ = 60
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")
if vse_norm:
    d = int(input("Оцените ваши финансовые знания по шкале от 1 до 5, где:"
                  "\n 1 - Нет финансовых знаний"
                  "\n 2 - Покупал ценные бумаги"
                  "\n 3 - Получал оброзование в финансовой сфере)"
                  "\n 4 - Работаю в финаносовой сфере"
                  "\n 5 - Получил(а) международный сертификат(CFA, ACCA и т.д.)\n"))
    if 1 <= d <= 5:
        if d == 3:
            fin = 0.8
        elif d == 2:
            fin = 0.5
        elif d == 1:
            fin = 0.2
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")
if vse_norm:
    f = int(input("""Представьте, что Вам надо купить оборудование для нового бизнес проекта, который начинаете 
    с нуля. Вы нашли два варианта, которые могут быть приобретены по разным ценам и с разными показателями устойчивости.
     Устройство A стоит значительно дешевле, но оно более ненадежно и непредсказуемо; 
     прибыль его может варьироваться - от 400 до 1 200$. Устройство B дороже, но гарантирует прибыль в размере 750$.
      Какое устройство выберете?
      1) Устройство A
      2) Устройство B
      """))
    if f == 1:
        k_risk += 0.45
    elif f == 2:
        k_risk += 0.1
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")
if vse_norm:
    g = int(input("""Вы уже инвестировали в акции компании, которая на данный момент имеет 
    хорошие перспективы роста. Однако, на фоне последних новостей, акции компании начали значительно падать.
     Как вы поступите в данной ситуации?
    1) Продам акции, чтобы избежать дальнейших потерь 
    2) Ничего не стану делать
    3) Немедленно докуплю на просадке, чтобы усреднить позицию
    """))
    if g == 1:
        k_risk += 0
    elif g == 2:
        k_risk += 0.3
    elif g == 3:
        k_risk += 0.7
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")
if vse_norm:
    h = int(input("""Какую цель вы преследуете, когда инвестируете?
    1) Сохранность денег от инфляции
    2) Создание финансовой подушки безопасности
    3) Стабильный пассивный доход в дополнении к основному
    4) Основной источник заработка
    """))
    if h == 1:
        k_hor += 1
    elif h == 2:
        k_hor += 0.8
    elif h == 3:
        k_hor += 0.5
    elif h == 4:
        k_hor += 0.1
    else:
        vse_norm = False
        print("Ошибка, вы ввели некорректное значение")
    with open('input.txt', 'w') as f:
        risk__ /= 100
        hor__ /= 7
        # print(f"risk = {risk__}")
        # print(f"hor = {hor__}")
        hor__ = (hor__ * fin + k_hor * 0.3) / (fin + k_hor * 0.3)
        risk__ = fin * (risk__ * fin + 0.3 * k_risk / 2) / (fin + k_risk * 0.3)
        # print(f"risk = {risk__}")
        # print(f"hor = {hor__}")
        risk__ = int(risk__ * 100)
        hor__ = int(hor__ * 7)
        f.write(f'{risk__} {hor__} {time__}')
    main_()