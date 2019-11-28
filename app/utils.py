def distance(me, thing):
  x_distance = abs(me['x']-thing['x'])
  y_distance = abs(me['y']-thing['y'])

  return x_distance + y_distance

def within_one(body_part, x, y, me):
  for my_body_part in me['body']:
    if my_body_part['x'] == body_part['x'] and my_body_part['y'] == body_part['y']:
      return False

  return (abs(body_part['x'] - x) <= 2 and abs(body_part['y'] - y) <= 2)

def is_safe(data, x, y, check_super_safe=False, check_head_safe=False):
  if x >= data['board']['height'] or y >= data['board']['height'] or x < 0 or y < 0:
    return False

  me = data['you']

  for snake in data['board']['snakes']:
    for body_part in snake['body']:
      if check_super_safe and within_one(body_part, x, y, me) and len(me['body']) <= len(snake['body']):
        return False
      elif check_head_safe and within_one(snake['body'][0], x, y, {'body': [me['body'][0]]}):
        return False
      elif body_part['x'] == x and body_part['y'] == y and len(me['body']) <= len(snake['body']):
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

  if food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_super_safe=True):
    print('*** Super safe food right')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_super_safe=True):
    print('*** Super safe food left')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_super_safe=True):
    print('*** Super safe food down')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_super_safe=True):
    print('*** Super safe food up')
    return 'up'
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_head_safe=True):
    print('*** Super safe head food right')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_head_safe=True):
    print('*** Super safe head food left')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_head_safe=True):
    print('*** Super safe head food down')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_head_safe=True):
    print('*** Super safe head food up')
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_super_safe=True):
    print('*** Super safe right')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_super_safe=True):
    print('*** Super safe left')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_super_safe=True):
    print('*** Super safe down')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_super_safe=True):
    print('*** Super safe up')
    return 'up'
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y']):
    print('*** Safe food right')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y']):
    print('*** Safe food left')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1):
    print('*** Safe food down')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1):
    print('*** Safe food up')
    return 'up'
  elif is_safe(data, me['x']+1, me['y']):
    print('*** Safe right')
    return 'right'
  elif is_safe(data, me['x']-1, me['y']):
    print('*** Safe left')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1):
    print('*** Safe down')
    return 'down'
  else:
    print('*** Nothing safe, go up and die')
    return 'up'
