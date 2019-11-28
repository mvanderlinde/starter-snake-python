def distance(me, thing):
  x_distance = abs(me['x']-thing['x'])
  y_distance = abs(me['y']-thing['y'])

  return x_distance + y_distance

def is_safe(data, x, y):
  if x >= data['board']['height'] or y >= data['board']['height'] or x < 0 or y < 0:
    return False

  for snake in data['board']['snakes']:
    for body_part in snake['body']:
      if body_part['x'] == x and body_part['y'] == y:
        return False

  return True

def find_closest_food(data):
  closest_distance = 1000 # Set closest to large number to start
  closest_food = None

  for food in data['board']['food']:
    current_distance = distance(data['you']['body'][0], food)

    if current_distance < closest_distance:
      closest_distance = current_distance
      closest_food = food

  return closest_food

def which_way(data, food):
  me = data['you']['body'][0]

  if me['x'] < food['x'] and is_safe(data, me['x']+1, me['y']):
    return 'right'
  elif me['x'] > food['x'] and is_safe(data, me['x']-1, me['y']):
    return 'left'
  elif me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1):
    return 'down'
  elif me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1):
    return 'up'
  elif is_safe(data, me['x']+1, me['y']):
    return 'right'
  elif is_safe(data, me['x']-1, me['y']):
    return 'left'
  elif is_safe(data, me['x'], me['y']+1):
    return 'down'
  else:
    return 'up'
