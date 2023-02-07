import enum
from random import randint


class Order(enum.Enum):
    '''кто ходит'''
    player = 0
    cpu = 1


class Game:
    '''
    игра спички
    на столе 50 спичек
    за ход можно забрать не более 8 спичек
    выигрывает то, забрал последние спички со стола
    '''
    help = ('Игра 50 спичек.\n'
            'Правила: на столе лежат 50 спичек. Каждый по очереди берет из кучки от одной до восьми спичек\n'
            'Выигрывает тот, кто заберет последние спички из кучки')

    heap: int  # куча спичек
    gamestatus: bool  # состояние игры

    def __init__(self):
        self.gamestatus = False
        '''начальное состояние игры (остановлена)'''
        self.heap = 50
        '''число спичек в куче'''
        self.act = Order.player
        '''чей ход: cpu/player'''

    def start(self):
        """старт игры
        """
        self.gamestatus = True
        self.heap = 50

    def stop(self):
        """остановка игры
        """
        self.gamestatus = False

    def action_player(self, count_items):
        """ход игрока
        Args:
            count_items (int): число спичек, которые взял игрок
        """
        if self.gamestatus:
            # игрок сделал ход
            self.heap -= count_items
            return
        else:
            pass

    def action_cpu(self):
        """ход компьютера
        Returns:
            int : число спичек, которые взял компьютер
        """
        if self.gamestatus:
            if self.heap <= 8:
                # компьютер выиграл
                count = self.heap
                self.heap = 0
                return count
            elif 9 < self.heap < 18:
                # предвыигрышный ход
                count = self.heap-9
                self.heap -= count
                return count
            else:
                # обычный ход
                count = randint(1, 8)
                self.heap -= count
                return count
        else:
            return 0

    def check_game_state(self):
        """проверка на конец игры (0 спичек)
        Returns:
            True: конец игры (спички не закончилсь)
            False: игра продолжается (спички не закончилсь)
        """
        return self.heap == 0