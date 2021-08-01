from flask import Flask, render_template
app = Flask(__name__)

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

def should_do(chore):
  # Calculates the amount of time since the last completion time
  # and returns whether or not it goes on the todo list.
  days_since_completion = (int(time.time()) - chore['last_completed']) / (60 * 60 * 24)
  return days_since_completion - frequencies[chore['frequency']] > 0

def get_chores():
  with open(chore_file) as f:
    chore_list = json.load(f)

  # Calculate the todo and done lists
  todo = []
  done = []
  for chore in chore_list:
    if should_do(chore):
      todo.append(chore)
    else:
      done.append(chore)

  # Sort the chores by priority
  return {'todo': sorted(todo, key=lambda chore: frequencies[chore['frequency']], reverse=True),
          'done': sorted(done, key=lambda chore: frequencies[chore['frequency']], reverse=True)}

def dismiss_chore(dismissed_chore):
  with open(chore_file) as f:
    chore_list = json.load(f)
  for chore in chore_list:
    if chore['chore_name'] != dismissed_chore:
      continue
    now = int(time.time())
    chore['last_completed'] = now
    chore['next_due_date'] = now + frequencies[chore['frequency']] * 60 * 60 * 24
  with open(chore_file, 'w') as f:
    json.dump(chore_list, f, ensure_ascii=True, indent=2, sort_keys=True)

@app.route('/')
def hello(name=None):
  chores = get_chores()
  return render_template(
    'index.html', 
    todo_chores=chores['todo'], 
    done_chores=chores['done'])

@app.route('/dismiss/<chorename>')
def request_chore_dismiss(chorename):
	dismiss_chore(chorename)
