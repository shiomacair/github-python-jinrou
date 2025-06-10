"""
status_key = ["player_list",
              "PLAYER_LIST_REPORT", 
              "uranai_taishou", 
              "goei_taishou_list", 
              "attacker_name", 
              "attack_taishou_list", 
              "giseihsa_list", 
              "shokei_taishou", 
              "day_count"]
"""
import random
import statistics
from tkinter import messagebox, simpledialog


# 属性
NINGEN = ["村人", "占い師", "霊能者", "狩人", "共有者", "ポンコツ", "狂人", "背徳者"]
JINROU = ["人狼"]
YOUKO = ["妖狐"]


# 役職
class Player():
    """Player のインスタンスは作っちゃだめ (self.job がないため)"""
    def __init__(self, name):
        self.name = name
        if self.job in NINGEN:
            self.zokusei = "人間"
        elif self.job in JINROU:
            self.zokusei = "人狼"
        elif self.job in YOUKO:
            self.zokusei = "妖狐"
        else:
            raise ValueError(f"{self.job} には属性が定義されていません。")

    def display_job(self, status):
        messagebox.showinfo(f"{self.name}", f"あなたは {self.job} です。")

    def job_skill(self, status):
        messagebox.showinfo("スキル", "スキルはありません。")
        return status


class Murabito(Player):
    def __init__(self, name):
        self.job = "村人"
        super().__init__(name)


class Uranaishi(Player):
    def __init__(self, name):
        self.job = "占い師"
        super().__init__(name)

    def display_job(self, status):
        super().display_job(status)
        if status["day_count"] == 0:
            player_list_without_you = [p for p in status["player_list"] if p.name != self.name]
            uranai_taishou = random.choice(player_list_without_you)
            is_jinrou(uranai_taishou)

    def job_skill(self, status):
        messagebox.showinfo("スキル", "誰か一人を選んで、人狼 かどうか調べます。\n次のページで占う相手を選んでください。")
        status["uranai_taishou"] = uranai(self.name, status["player_list"])
        return status


class Reinousha(Player):
    def __init__(self, name):
        self.job = "霊能者"
        super().__init__(name)

    def job_skill(self, status):
        messagebox.showinfo("スキル", f"処刑された {status['shokei_taishou'].name} が 人狼 かどうか調べます。")
        reinou(status["shokei_taishou"])
        return status


class Karyuudo(Player):
    def __init__(self, name):
        self.job = "狩人"
        super().__init__(name)

    def job_skill(self, status):
        messagebox.showinfo("スキル", "誰か一人を選んで、人狼 の襲撃から護ります。\n次のページで護衛する相手を選んでください。")
        status["goei_taishou_list"].append(goei(self.name, status["player_list"]))
        return status


class Kyouyuusha(Player):
    def __init__(self, name):
        self.job = "共有者"
        super().__init__(name)

    def display_job(self, status):
        super().display_job(status)
        kyouyuusha_name_list = [p.name for p in status["player_list"] if p.job == "共有者"]
        messagebox.showinfo(f"{self.name}", f"生存している 共有者 は、{kyouyuusha_name_list} です。")


class Ponkotsu(Player):
    def __init__(self, name):
        self.job = "ポンコツ"
        super().__init__(name)
        self.fake_job = random.choice(["占い師", "霊能者", "狩人"])

    def display_job(self, status):
        messagebox.showinfo(f"{self.name}", f"あなたは {self.fake_job} です。")
        if self.fake_job == "占い師" and status["day_count"] == 0:
            player_list_without_you = [p for p in status["player_list"] if p.name != self.name]
            uranai_taishou = random.choice(player_list_without_you)
            messagebox.showinfo(f"{self.name}", f"{uranai_taishou.name} は 人狼 ではありません。")

    def job_skill(self, status):
        player_list_without_you = [p for p in status["player_list"] if p.name != self.name]
        if self.fake_job == "占い師":
            messagebox.showinfo("スキル", "誰か一人を選んで、人狼 かどうか調べます。\n次のページで占う相手を選んでください。")
            uranai_taishou = select_player(player_list_without_you)
            messagebox.showinfo("人狼判定", f"{uranai_taishou.name} は 人狼 ではありません。")
        if self.fake_job == "霊能者":
            messagebox.showinfo("スキル", f"処刑された {status['shokei_taishou'].name} が 人狼 かどうか調べます。")
            messagebox.showinfo(f"{self.name}", f"{status['shokei_taishou'].name} は 人狼 ではありません。")
        if self.fake_job == "狩人":
            messagebox.showinfo("スキル", "誰か一人を選んで、人狼 の襲撃から護ります。\n次のページで護衛する相手を選んでください。")
            select_player(player_list_without_you)
        return status


class Kyoujin(Player):
    def __init__(self, name):
        self.job = "狂人"
        super().__init__(name)


class Jinrou(Player):
    def __init__(self, name):
        self.job = "人狼"
        super().__init__(name)

    def display_job(self, status):
        super().display_job(status)
        jinrou_name_list = [p.name for p in status["player_list"] if p.zokusei == "人狼"]
        messagebox.showinfo(f"仲間の人狼を表示", f"生存している 人狼 は、{jinrou_name_list} です。")

    def job_skill(self, status):
        if self.name == status["attacker_name"]:
            messagebox.showinfo("スキル", "誰か一人を選んで、襲撃します。\n次のページで襲撃する相手を選んでください。")
            status["attack_taishou_list"].append(attack(status["player_list"]))
        else:
            messagebox.showinfo("スキル", f"今夜の襲撃は {status['attacker_name']} が行います。")
        return status


class Haitokusha(Player):
    def __init__(self, name):
        self.job = "背徳者"
        super().__init__(name)

    def display_job(self, status):
        super().display_job(status)
        youko_name_list = [p.name for p in status["player_list"] if p.zokusei == "妖狐"]
        messagebox.showinfo(f"{self.name}", f"生存している 妖狐 は、{youko_name_list} です。")


class Youko(Player):
    def __init__(self, name):
        self.job = "妖狐"
        super().__init__(name)


# メインゲーム
def main_game():
    ninzuu = set_ninzuu()
    status = start_game(ninzuu)
    status["day_count"] = 0
    first_action(status)
    status["day_count"] += 1
    announce_asa(status["day_count"])
    while True:
        announce_start_kaigi()
        announce_touhyou()
        touhyou_top = touhyou(status["player_list"])
        status = shokei(touhyou_top, status)
        announce_seizonsha(status)
        gameset = is_gameset(status["player_list"])
        if gameset != 0:
            break
        announce_yoru()
        status = decide_attacker(status)
        status = create_giseisha_list(use_skills(status))
        status["day_count"] += 1
        announce_asa(status["day_count"])
        status = kill_giseisha(status)
        status = jisatsu(status)
        announce_seizonsha(status)
        gameset = is_gameset(status["player_list"])
        if gameset != 0:
            break
    announce_winner(gameset)
    announce_jobs(status)


# メッセージ表示
def announce_asa(day_count):
    messagebox.showinfo("朝", f"{day_count}日目の朝になりました。")


def announce_start_kaigi():
    messagebox.showinfo("会議", "会議を始めます。\n会議が終わったら、Enter を押してください。")


def announce_touhyou():
    messagebox.showinfo("投票", "投票を行います。")


def announce_yoru():
    messagebox.showinfo("夜", "夜になりました。")


def announce_giseisha(giseiha):
    messagebox.showinfo("犠牲者", f"{giseiha} が死んでしまいました。")


def announce_seizonsha(status):
    seizonsha_name_list = [p.name for p in status["player_list"]]
    messagebox.showinfo("生存者", f"残りのプレイヤーは {seizonsha_name_list} です。")


def announce_winner(gameset):
    if gameset == 1:
        messagebox.showinfo("勝者", "村人陣営の勝利です。")
    elif gameset == 2:
        messagebox.showinfo("勝者", "人狼陣営の勝利です。")
    elif gameset == 3:
        messagebox.showinfo("勝者", "妖狐陣営の勝利です。")


def announce_jobs(status):
    report = ""
    for p in status["PLAYER_LIST_REPORT"]:
        report += f"{p.name} => {p.job}\n"
    messagebox.showinfo("役職レポート", report)


# ゲーム開始時に使う
def set_ninzuu():
    ninzuu = int(simpledialog.askstring("人数", "何人で遊ぶかを入力してください。 (5人~15人)"))
    while True:
        if 5 <= ninzuu <= 15:
            break
        ninzuu = int(simpledialog.askstring("人数", "人数は5人から15人までです。\n何人で遊ぶかを入力してください。"))
    return ninzuu


def start_game(ninzuu):
    status = {"player_list": []}
    p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15 = 1,2,3,4,5,6,7,8,9,0,1,2,3,4,5
    player_list_dummy = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12,p13,p14,p15]
    jobs = ([Murabito] + [Murabito] + [Uranaishi] + [Kyoujin] + [Jinrou] +
            [Reinousha] + [Jinrou] + [Karyuudo] + [Youko] + [Haitokusha] +
            [Kyouyuusha] + [Kyouyuusha] + [Jinrou] + [Murabito] + [Ponkotsu])
    jobs = jobs[0:ninzuu]
    random.shuffle(jobs)
    name_list = create_name_list(ninzuu)
    for player, job , name in zip(player_list_dummy, jobs, name_list):
        player = job(name)
        status["player_list"].append(player)
    status["PLAYER_LIST_REPORT"] = [p for p in status["player_list"]]
    return status


def create_name_list(ninzuu):
    name_list = []
    for i in range(1, ninzuu + 1):
        name = input_name(name_list, i)
        name_list.append(name)
    return name_list


def input_name(name_list, i):
    name = simpledialog.askstring(f"{i}人目", f"{i}人目のプレイヤーの名前を入力してください。")
    while True:
        if name not in name_list:
            return name
        name = simpledialog.askstring(f"{i}人目", f"{name} はすでに登録されています。\n他の名前を使用してください。")


def first_action(status):
    for p in status["player_list"]:
        messagebox.showinfo(f"{p.name}", f"{p.name} は Enter を押してください。\n他の人は画面を見ないでください。")
        p.display_job(status)
        messagebox.showinfo(f"{p.name}", "行動を終わります。\nEnter を押してください。")


# ゲームの途中で使う
def touhyou(player_list):
    touhyou_kekka = []
    for you in player_list:
        messagebox.showinfo(f"{you.name} 投票", f"{you.name} の投票です。\n次のページで投票する相手を選んでください。")
        player_list_without_you = [p for p in player_list if p != you]
        touhyou_kekka.append(select_player(player_list_without_you))
    touhyou_top = random.choice(statistics.multimode(touhyou_kekka))
    return touhyou_top


def shokei(touhyou_top, status):
    status["shokei_taishou"] = touhyou_top
    messagebox.showinfo("処刑", f"{touhyou_top.name} が処刑されました。")
    status["player_list"].remove(touhyou_top)
    return status


def select_player(player_list):
    selected = simpledialog.askstring(f"select", f"{[p.name for p in player_list]}")
    while True:
        for p in player_list:
            if p.name == selected:
                selected = p
        if selected in player_list:
            return selected
        selected = simpledialog.askstring(f"select", f"{selected} はいません。\n{[p.name for p in player_list]}")


def create_giseisha_list(status):
    status["giseisha_list"] = [attack_taishou for attack_taishou in status["attack_taishou_list"] if attack_taishou not in status["goei_taishou_list"] and attack_taishou.zokusei != "妖狐"]
    if status["uranai_taishou"] != 0:
        if status["uranai_taishou"].zokusei == "妖狐":
            status["giseisha_list"].append(status["uranai_taishou"])
    random.shuffle(status["giseisha_list"])
    return status


def kill_giseisha(status):
    if len(status["giseisha_list"]) == 0:
        messagebox.showinfo("犠牲者", "昨夜の犠牲者はいませんでした。")
        return status
    for p in status["giseisha_list"]:
        status["player_list"].remove(p)
        announce_giseisha(p.name)
    return status


def use_skills(status):
    status["attack_taishou_list"] = []
    status["goei_taishou_list"] = []
    status["uranai_taishou"] = 0
    for p in status["player_list"]:
        messagebox.showinfo(f"{p.name}", f"{p.name} は Enter を押してください。\n他の人は画面を見ないでください。")
        p.display_job(status)
        status = p.job_skill(status)
        messagebox.showinfo(f"{p.name}", "行動を終わります。\nEnter を押してください。")
    return status


def is_gameset(player_list):
    ningen_list = [p for p in player_list if p.zokusei == "人間"]
    jinrou_list = [p for p in player_list if p.zokusei == "人狼"]
    if len(jinrou_list) == 0:
        gameset = 1
    elif len(ningen_list) <= len(jinrou_list):
        gameset = 2
    else:
        gameset = 0
    if gameset != 0:
        youko_list = [p for p in player_list if p.zokusei == "妖狐"]
        if len(youko_list) != 0:
            gameset = 3
    return gameset


# 役職ごとの能力
def uranai(your_name, player_list):
    player_list_without_you = [p for p in player_list if p.name != your_name]
    uranai_taishou = select_player(player_list_without_you)
    is_jinrou(uranai_taishou)
    return uranai_taishou


def reinou(shokei_taishou):
    is_jinrou(shokei_taishou)


def is_jinrou(player):
    if player.zokusei == "人狼":
        messagebox.showinfo("人狼判定", f"{player.name} は 人狼 です。")
    else:
        messagebox.showinfo("人狼判定", f"{player.name} は 人狼 ではありません。")


def goei(your_name, player_list):
    player_list_without_you = [p for p in player_list if p.name != your_name]
    goei_taishou = select_player(player_list_without_you)
    return goei_taishou


def attack(player_list):
    player_list_without_jinrou = [p for p in player_list if p.zokusei != "人狼"]
    attack_taishou = select_player(player_list_without_jinrou)
    return attack_taishou


def decide_attacker(status):
    jinrou_name_list = [p.name for p in status["player_list"] if p.zokusei == "人狼"]
    status["attacker_name"] = random.choice(jinrou_name_list)
    return status


def jisatsu(status):
    haitokusha_list = [p for p in status["player_list"] if p.job == "背徳者"]
    youko_list = [p for p in status["player_list"] if p.zokusei == "妖狐"]
    if youko_list == []:
        for p in haitokusha_list:
            messagebox.showinfo("自殺", f"{p.name} が自殺しました。")
            status["player_list"].remove(p)
    return status


if __name__ == "__main__":
    main_game()

