class Observable:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def detach(self, observer):
        self.observers.append(observer)

    def notifyAll(self, money, mesaj):
        for element in self.observers:
            element.update(money, mesaj)


class DisplayObserver:
    def update(self, money, mesaj=None):
        if money:
            print("S-au introdus {} bani".format(money))


class ChoiceObserver:
    def update(self, money=0, mesaj=None):
        if mesaj:
            print(mesaj)


class SelectProductSTM(Observable):
    def __init__(self):
        super().__init__()
        self.select_product_state = SelectProduct(self)
        self.coca_cola_state = CocaCola(self, 300)
        self.pepsi_state = Pepsi(self, 400)
        self.sprite_state = Sprite(self, 500)
        self.current_state = State()

    def choose_another_product(self):
        self.select_product_state.choose()


class State:
    pass


class SelectProduct(State):
    def __init__(self, state_machine: SelectProductSTM, price=0):
        self.state_machine = state_machine
        self.price = price

    def choose(self):
        name = input("Apasati tasta 1 pentru CocaCola, tasta 2 pentru Pepsi, tasta 3 pentru Sprite: ")
        if name == "1":
            self.state_machine.select_product_state = self.state_machine.coca_cola_state
        elif name == "2":
            self.state_machine.select_product_state = self.state_machine.pepsi_state
        elif name == "3":
            self.state_machine.select_product_state = self.state_machine.sprite_state
        else:
            print("Apasati o tasta cu optiune valida")
            return


class CocaCola(State):
    def __init__(self, state_machine: SelectProductSTM, price):
        self.state_machine = state_machine
        self.price = price


class Pepsi(State):
    def __init__(self, state_machine: SelectProductSTM, price):
        self.state_machine = state_machine
        self.price = price


class Sprite(State):
    def __init__(self, state_machine: SelectProductSTM, price):
        self.state_machine = state_machine
        self.price = price


class TakeMoneySTM:
    def __init__(self):
        self.wait_state = WaitingForClient(self)
        self.insert_money_state = InsertMoney(self)
        self.current_state = self.wait_state
        self.money = 0

    def add_money(self, value):
        self.money += value

    def update_amount_of_money(self, value):
        pass


class WaitingForClient(State):
    def __init__(self, state_machine: TakeMoneySTM):
        self.state_machine = state_machine

    def client_arrived(self):
        self.state_machine.current_state = self.state_machine.insert_money_state


class InsertMoney(State):
    def __init__(self, state_machine: TakeMoneySTM):
        self.state_machine = state_machine

    def insert_10bani(self):
        self.state_machine.add_money(10)

    def insert_50bani(self):
        self.state_machine.add_money(50)

    def insert_1leu(self):
        self.state_machine.add_money(100)

    def insert_5lei(self):
        self.state_machine.add_money(500)

    def insert_10lei(self):
        self.state_machine.add_money(1000)


class VendingMachineSTM:
    def __init__(self, observer):
        self.take_money_stm = TakeMoneySTM()
        self.select_product_stm = SelectProductSTM()
        self.observer = observer

    def proceed_to_checkout(self):
        if self.select_product_stm.select_product_state.price <= self.take_money_stm.money:
            self.select_product_stm = SelectProductSTM()
            self.take_money_stm.current_state = self.take_money_stm.wait_state
            self.observer.notifyAll(money = 0, mesaj = "Ridicati bautura!")
        else:
            self.observer.notifyAll(money = self.take_money_stm.money, mesaj = "Insuficienti bani pentru produsul selectat")
            self.take_money_stm.current_state = self.take_money_stm.insert_money_state


if __name__ == '__main__':
    observ = Observable()
    observ.attach(ChoiceObserver())
    observ.attach(DisplayObserver())

    VendingMachine = VendingMachineSTM(observ)

    VendingMachine.select_product_stm.choose_another_product()
    
    VendingMachine.take_money_stm.insert_money_state.insert_1leu()
    VendingMachine.proceed_to_checkout()

    VendingMachine.take_money_stm.insert_money_state.insert_1leu()
    VendingMachine.proceed_to_checkout()

    VendingMachine.take_money_stm.insert_money_state.insert_5lei()
    VendingMachine.proceed_to_checkout()