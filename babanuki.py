from pydantic import BaseModel
import random


class Player(BaseModel):
    """
    プレイヤーを作成します。
    """

    name: str
    deck: list[str] = []
    is_win: bool = False
    is_auto: bool = True


class Dealer:

    def __init__(self):
        self.initial_deck = self.create_initial_deck()

    def create_initial_deck(self) -> list:
        """
        53枚のカードを含むリストを作成します。
        Xカードはババ(ジョーカー)を表します。
        """
        # list
        initial_deck = []

        # 1~13
        for n in range(1, 14):
            # egara (str)
            if n == 1:
                egara = "A"
            elif n == 11:
                egara = "J"
            elif n == 12:
                egara = "Q"
            elif n == 13:
                egara = "K"
            else:
                egara = str(n)

            initial_deck.append(egara)

        # 4種類
        initial_deck = initial_deck * 4

        # ババ(ジョーカー)の追加
        initial_deck.append("X")

        return initial_deck

    def initial_deal(self, players: list[Player]) -> list[Player]:
        """
        各プレイヤーへカードを配ります。
        """
        random.shuffle(self.initial_deck)
        q, mod = divmod(len(self.initial_deck), len(players))
        for i, player in enumerate(players):
            slice_n = q + 1 if i < mod else q
            player.deck = self.initial_deck[:slice_n]
            del self.initial_deck[:slice_n]
        return players

    def initial_putdown(self, deck: list) -> list:
        """
        重複したカードを捨てます。
        """
        while len(set(deck)) != len(deck):
            popped_card = deck.pop(0)
            if popped_card in deck:
                deck.remove(popped_card)
            else:
                deck.append(popped_card)
        return deck


class Babanuki:

    def __init__(self, players: list):
        self.players = players

    def create_turn_index(self, passer_i: int, taker_i: int) -> tuple:
        """
        カードを引く人/渡す人を決定します。
        """
        passer_i = taker_i
        taker_i += 1
        if passer_i >= len(self.players):
            passer_i = 0
            taker_i = 1
        elif taker_i >= len(self.players):
            taker_i = 0
        return passer_i, taker_i

    def select(self, passer: Player, taker: Player) -> str:
        """
        カードを引きます。
        """
        # is_auto == True
        if taker.is_auto:
            select_index = random.randrange(len(passer.deck))
        else:
            # is_auto == False
            while True:
                text = ""
                for n in range(len(passer.deck)):
                    text += f"[{n+1}]"
                select_index = input(f"カードを引いてください。 {text}:")
                try:
                    select_index = int(select_index) - 1
                    if select_index < 0 or select_index >= len(passer.deck):
                        raise IndexError()
                except ValueError:
                    print("\t整数を入力してください!")
                except IndexError:
                    print("\t正しい数字を選択してください!")
                else:
                    break
            print(f"\あなたは {select_index+1}番目のカードを選択しました。")
        selected_card = passer.deck.pop(select_index)
        return selected_card

    def putdown_or_add(self, selected_card: str, taker: Player):
        """ """
        try:
            taker.deck.remove(selected_card)
        except ValueError:
            taker.deck.append(selected_card)

    def run(self):
        """
        ゲームをスタートします。
        """
        passer_i = -1
        taker_i = 0
        loop = 0
        rank = []

        print("\n\n --- GAME START --- \n")

        while True:
            loop += 1
            print(f"\n --- TURN {loop} ---")

            passer_i, taker_i = self.create_turn_index(passer_i, taker_i)

            selected_card = self.select(players[passer_i], players[taker_i])

            self.putdown_or_add(selected_card, players[taker_i])

            print("\t現在の手札枚数: ", end="")
            for i in range(len(players)):
                print(f"{players[i].name}:{len(players[i].deck)}", end=" ")
                if len(players[i].deck) == 0:
                    print("WIN!", end="")
                    rank.append(players.pop(i))
                    break

            if len(players) < 2:
                break

        rank.append(players.pop())

        print("\n\n --- GAME END --- \n")
        for i in range(len(rank)):
            print(f" {i+1}位: {rank[i].name}")


dealer = Dealer()
# プレイヤーの作成
player1 = Player(name="A", is_auto=False)
player2 = Player(name="B")
player3 = Player(name="C")

# プレイヤーリストへ格納
players = dealer.initial_deal([player1, player2, player3])

# 重複したカードを捨てる
for i in range(len(players)):
    players[i].deck = dealer.initial_putdown(players[i].deck)

babanuki = Babanuki(players)
babanuki.run()
