from flask import Flask, render_template
app = Flask(__name__)

import os.path
import json
import time

chore_file = "sausage.json"

if not os.path.exists(chore_file):
  with open("example.json") as example_file:
    with open(chore_file, 'w') as out_file:
      out_file.write(example_file.read())
    
frequencies = {
  "daily": 1,
  "weekly": 7,
  "biweekly": 14,
  "monthly": 30,
  "bimonthly": 60,
}

minutes_in_day = 60 * 60 * 24

def should_do(chore):
  # Calculates the amount of time since the last completion time
  # and returns whether or not it goes on the todo list.
  days_since_completion = (int(time.time()) - chore['last_completed']) / minutes_in_day
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
    chore['next_due_date'] = now + frequencies[chore['frequency']] * minutes_in_day
  with open(chore_file, 'w') as f:
    json.dump(chore_list, f, ensure_ascii=True, indent=2, sort_keys=True)

# This looks for the most recently completed chore and resets
# the last_completed to 1-day more than the frequency, so that it
# shows up on the todo list again.
def undo_last_chore():
  with open(chore_file) as f:
    chore_list = json.load(f)
  sorted_chores = sorted(chore_list, key=lambda chore: chore['last_completed'], reverse=True)
  last_chore = sorted_chores[0]["chore_name"]
  for chore in chore_list:
    if chore['chore_name'] != last_chore:
      continue
    now = int(time.time())
    chore['last_completed'] = now - (frequencies[chore['frequency']] + 1) * minutes_in_day
    chore['next_due_date'] = now - minutes_in_day
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

@app.route('/undo')
def request_undo():
  undo_last_chore()