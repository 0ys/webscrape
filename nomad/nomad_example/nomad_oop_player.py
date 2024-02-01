class Player:

    def __init__(self, name, team):
        self.name = name
        self.xp = 1500
        self.team = team

    def introduce(self):
        print(f"Hello! I'm {self.name} and I play for {self.team}")

class Team:

    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []
    
    def add_player(self, name):
        new_player = Player(name, self.team_name)
        self.players.append(new_player)

    def show_players(self):
        for player in self.players:
            player.introduce()

    def remove_player(self, name):
        for player in self.players:
            if player.name == name:
                self.players.remove(player)
            else:
                print("Player Not Found")

    def show_total_xp(self):
        total_xp = 0
        for player in self.players:
            total_xp += player.xp
        print(f"Total XP of {self.team_name} is {total_xp}")



team_x = Team("Team X")
team_x.add_player("Nico")
team_x.add_player("ysgong")

team_blue = Team("Team Blue")
team_blue.add_player("Lynn")
team_blue.add_player("gong")

team_x.show_players()
team_x.show_total_xp()

team_blue.show_players()
team_blue.show_total_xp()

team_blue.remove_player("gong")
team_blue.show_players()