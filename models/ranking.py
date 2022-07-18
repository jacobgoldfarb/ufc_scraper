class Ranking:
    
    def __init__(self, division, ordered_fighters):
        self.division = division
        self.ordered_fighters = ordered_fighters
        self.ranked_list = [f"{i + 1}. {fighter}" for (i, fighter) in enumerate(self.ordered_fighters)]
        
    def __str__(self):
        return self.division + "\n" + f"\n".join(self.ranked_list)