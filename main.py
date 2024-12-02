class Election:
    def __init__(self, candidate_choice):
        self.candidate = candidate_choice
        self.opponent = "D" if candidate_choice == "R" else "R"
        self.percent_to_win = 0.5000001

    def display_current_standings(self, d_votes, r_votes, total_votes):
        print("-" * 50)
        print(f"Current D Standing: {self.calculate_percentage(d_votes, total_votes)}%")
        print(f"Current R Standing: {self.calculate_percentage(r_votes, total_votes)}%")
        print("-" * 50)

    def calculate_percentage(self, part, whole):
        return round((part / whole) * 100, 3)

    def get_estimated_votes_left(self, total_votes_counted, percent_counted):
        votes_per_percent = total_votes_counted / percent_counted
        percent_remaining = 100 - percent_counted
        return round_up(votes_per_percent * percent_remaining)

    def evaluate_win_possibility(self, candidate_votes, opponent_votes, estimated_votes_left, total_votes_counted, percent_counted):
        total_voting_population = estimated_votes_left + total_votes_counted

        total_votes_to_win = ((estimated_votes_left+total_votes_counted)*self.percent_to_win)
        additional_required_votes_to_win  = round_up(total_votes_to_win - candidate_votes) if total_votes_to_win - candidate_votes > 0 else 0
        additional_required_votes_to_lose = round_up(total_votes_to_win - opponent_votes)  if total_votes_to_win - opponent_votes  > 0 else 0
        print(f"Additional votes to win majority: {additional_required_votes_to_win}\n")
        
        if additional_required_votes_to_win >= 0:
            minimum_win_percentage = self.calculate_percentage(candidate_votes + additional_required_votes_to_win, total_voting_population)
        else:
            minimum_win_percentage = 0

        if (49 <= minimum_win_percentage <= 51) and (percent_counted > 90):
            # Tie/Recount
            return "Toss up. Potential recount."
        elif (estimated_votes_left > additional_required_votes_to_win) and (additional_required_votes_to_win == 0): 
            # Guaranteed Win
            return self.generate_win_message(candidate_votes, opponent_votes, estimated_votes_left, total_voting_population, guaranteed=True)
        elif (estimated_votes_left < additional_required_votes_to_win) and (additional_required_votes_to_lose == 0): 
            # Guaranteed Loss
            return self.generate_win_message(candidate_votes, opponent_votes, estimated_votes_left, total_voting_population, guaranteed=False)
        else:
            # Not enough information (Most likely condition during early-mid election)
            percent_left_needed = round((additional_required_votes_to_win / estimated_votes_left) * 100, 3)
            return f"Unclear Outcome - Minimum Remaining Votes to Win: {additional_required_votes_to_win} votes ({percent_left_needed}% of remaining ballots)"

    def generate_win_message(self, candidate_votes, opponent_votes, estimated_votes_left, total_voting_population, guaranteed):
        if guaranteed:
            header = "Guaranteed win."
            candidate_final_votes = candidate_votes
            opponent_final_votes  = opponent_votes + estimated_votes_left
        else:
            header = "Impossible to win."
            candidate_final_votes = candidate_votes + estimated_votes_left
            opponent_final_votes  = opponent_votes

        return (
            f"{header}\n"
            f"\tEven with remaining votes 100% going to the {'opponent' if guaranteed else 'candidate'}:\n"
            f"\t{self.candidate}: {candidate_final_votes} ({self.calculate_percentage(candidate_final_votes, total_voting_population)}%)\n"
            f"\t{self.opponent }: {opponent_final_votes } ({self.calculate_percentage(opponent_final_votes,  total_voting_population)}%)"
        )

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

def get_percentage(prompt):
    while True:
        p = get_integer(prompt)
        if 1 <= p <= 99:
            return p
        prompt = "Percentage Counted out of range. Select an integer between 1-99 inclusive: "

def get_candidate_choice(prompt):
    while True:
        choice = input(prompt).strip().upper()
        if choice in {"D", "R"}:
            return choice
        print("Invalid input. Please choose 'D' or 'R'.")

def round_up(i):
    return int(i) + bool(i % 1)

if __name__ == '__main__':
    candidate = get_candidate_choice("Choose your candidate (D or R): ")
    election = Election(candidate)

    while True:
        input("State: ")
        d_votes = get_integer("D Votes: ")
        r_votes = get_integer("R Votes: ")
        total_votes_counted = d_votes + r_votes

        percent_counted = get_percentage("Percent Reported (1-99): ")

        estimated_votes_left = election.get_estimated_votes_left(total_votes_counted, percent_counted)

        election.display_current_standings(d_votes, r_votes, total_votes_counted)

        print(f"Estimated Votes Left Uncounted: {estimated_votes_left}")

        candidate_votes = d_votes if candidate == "D" else r_votes
        opponent_votes  = r_votes if candidate == "D" else d_votes

        print(election.evaluate_win_possibility(candidate_votes, opponent_votes, estimated_votes_left, total_votes_counted, percent_counted))

        print("\n" + "=" * 75 + "\n")
