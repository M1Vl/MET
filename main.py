# нормировка для risk, horizont, monitor:
#    risk - [0,100],    horizont - [0,7],   monitor - [0, 40] ->
# -> risk - [0,1],      horizont - [0,1],   monitor - [0, 1]

k_risk = 18
k_horizont = 8
k_monitor = 11


# Объекты этого класса это как раз инвестиционные стратегии
class Portfolio:
    def __init__(self, name, stock, bond, currency, mif, risk=0, horizont=0, monitor=0):
        self.name = name
        self.stock = stock
        self.bond = bond
        self.currency = currency
        self.mif = mif
        self.risk = risk
        self.horizont = horizont
        self.monitor = monitor

    def equals_targets(self, _risk, _horizont, _monitor):
        # returns [0,1] (1 - full equal)
        a = 1 - (max(self.risk, _risk) - min(self.risk, _risk))
        b = 1 - (max(self.horizont, _horizont) - min(self.horizont, _horizont))
        c = 1 - (max(self.monitor, _monitor) - min(self.monitor, _monitor))
        global k_risk, k_horizont, k_monitor
        return (k_risk * a + k_horizont * b + k_monitor * (c if self.monitor > _monitor else 1)) / (k_risk + k_monitor + k_horizont)

    def equals_consists(self, other):
        # returns [0,1]  (1 - full equal)
        a = min(self.stock, other.stock)
        b = min(self.bond, other.bond)
        c = min(self.currency, other.currency)
        d = min(self.mif, other.mif)
        return a + b + c + d

    def __str__(self):
        return str(self.name + '\nАкции: ' + str(self.stock) + '\nОблигации: ' + str(
            self.bond) + '\nВалюта/Драг.Металы: ' + str(self.currency) + '\nФонды: ' + str(self.mif))


##############################################
def main_():
    Strategies = []
    # Считываем стратегии информация о которых записана в файле strats.txt
    f = open("strats.txt")
    for l in f:
        s = l.split()
        Strategies.append(Portfolio(s[0], float(s[1]) / 100, float(s[2]) / 100, float(s[3]) / 100, float(s[4]) / 100,
                                    float(s[5]) / 100, float(s[6]) / 7, float(s[7]) / 50))
    f.close()

    # Считываем параметры, полученные после прохождения теста, которые записаны в файле input.txt
    f = open("input.txt")

    risk_, horizont_, monitor_ = f.read().split()
    risk_ = float(risk_) / 100
    horizont_ = float(horizont_) / 7
    monitor_ = float(monitor_) / 50

    if risk_ >= 0.6:
        print(
            "В связи с вашей готовности к риску, предлагаем вам следующие стратегии на срочном рынке:\nСовмещенная стратегия (позволяет держать часть средств в акциях вдолгую, а другую часть использовать в маржинальной торговле)\n------------\nПозиционный трейдинг (для клиентов, имеющих опыт трейдинга и готовых рискнуть до 100% вложенных средств)")
    else:
        best_k = 0
        cur_best = 0
        for i in range(len(Strategies)):
            cur_k = Strategies[i].equals_targets(risk_, horizont_, monitor_)
            if cur_k > best_k:
                best_k = cur_k
                cur_best = i
        optimal_strategy = Strategies[cur_best]
        # print(best_k, '\n', optimal_strategy, sep='')
        print(optimal_strategy, sep='')
    f.close()
