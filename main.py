def intput(s):
	while True:
		try:
			i = int(input(s))
			return i
		except ValueError:
			print("Not a valid integer. Try again.")

def DorR(s):
	c = input(s)
	while c != "d" and c != "r":
		print("Invalid Input")
		c = input(s)
	return c


if __name__ == '__main__':
	candidate = DorR("Choose your candidate (d or r): ")
	c = None
	while(True):
		input("Location: ")
		d = intput("D Votes: ")
		r = intput("R Votes: ")
		counted = d+r

		p_done = intput("Percent Reported: ")
		p_left = 100-p_done

		one_percent = round(counted/p_done)

		votes_left = one_percent*p_left

		print("---------------------------------------------")
		print("Current D Standing:", round(d/counted*100,3), "%")
		print("Current R Standing:", round(r/counted*100,3), "%")
		print("---------------------------------------------")

		print("Estimated Votes Left:", votes_left)

		c = d if candidate == "d" else r

		winning_vote = (one_percent*50)-c

		if votes_left < winning_vote:
			print("Impossible to win.")
		elif winning_vote <= 0:
			print("Guaranteed win.")
		else:
			print("Minimum Remaining Votes to Win:", winning_vote, "votes -", round(winning_vote/votes_left*100, 3) , "%")

		print("=======================================================================")
