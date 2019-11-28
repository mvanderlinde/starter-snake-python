def distance(me, thing):
  x_distance = abs(me['x']-thing['x'])
  y_distance = abs(me['y']-thing['y'])

  return x_distance + y_distance

def within_one(body_part, x, y):
    return (abs(body_part['x'] - x) <= 2 and abs(body_part['y'] - y) <= 2)

def is_safe(data, x, y, check_super_safe=False):
  if x >= (data['board']['height']-1) or y >= (data['board']['height']-1) or x < 1 or y < 1:
    return False

  for snake in data['board']['snakes']:
    for body_part in snake['body']:
      if check_super_safe and not within_one(body_part, x, y):
        return True
      elif check_super_safe and within_one(body_part, x, y):
        return False
      elif body_part['x'] == x and body_part['y'] == y:
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

  if me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_super_safe=True):
    return 'right'
  elif me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_super_safe=True):
    return 'left'
  elif me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_super_safe=True):
    return 'down'
  elif me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_super_safe=True):
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_super_safe=True):
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_super_safe=True):
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_super_safe=True):
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_super_safe=True):
    return 'up'
  elif me['x'] < food['x'] and is_safe(data, me['x']+1, me['y']):
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
