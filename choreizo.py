import json
import time

chore_file = "sausage.json"

frequencies = {
	"daily": 1,
	"weekly": 7,
	"biweekly": 14,
	"monthly": 30,
	"bimonthly": 60,
}

class Chore:
	def __init__(self, name, description, frequency, last_completed = 0):
		self.name = name
		self.description = description
		# How often this chore should be done
		self.frequency_days = frequencies[frequency]
		# When this chore was last completed, in time since Epoch
		self.last_completed = last_completed

	def should_do(self):
		# Calculates the amount of time since the last completion time
		# and returns whether or not it goes on the todo list.
		days_since_completion = (int(time.time()) - self.last_completed) / (60 * 60 * 24)
		return days_since_completion - self.frequency_days > 0

def get_chores():
	with open(chore_file) as f:
		chore_list = json.load(f)

	# Calculate the todo list
	todo = []
	for chore in chore_list:
		if chore.should_do():
			todo.append(chore)

	# Sort the chores by priority
	return sorted(todo, key=lambda chore: chore.frequency_days, reverse=True)

def dismiss_chore(chore):
	with open(chore_file) as f:
		chore_list = json.load(f)

	chore_list[chore].last_completed = int(time.time())
	with open(chore_file, 'w') as f:
		json.dump(chore_list, f)