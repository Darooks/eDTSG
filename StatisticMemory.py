class StatisticMemory:
    voted_yes = 0
    voted_no = 0
    time_to_get_90_per = 0
    time_to_get_100_per = 0

    def set_voted_yes(self):
        self.voted_yes += 1

    def get_voted_yes(self):
        return self.voted_yes

    def set_voted_no(self):
        self.voted_no += 1

    def get_voted_no(self):
        return self.voted_no
