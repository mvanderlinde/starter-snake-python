closest_snake_distance = 1000
best_move = 'up'
best_move_distance = 0
best_move_coords = {
  'x': 0,
  'y': 0
}

def distance(me, thing):
  x_distance = abs(me['x']-thing['x'])
  y_distance = abs(me['y']-thing['y'])

  return x_distance + y_distance

def has_room(data, me, direction):
  available_space = 0

  my_length = len(me['body'])
  my_head = me['body'][0]
  if direction == 'left':
    for x in range(1,int(my_length/2)):
      for y in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']-y):
          available_space = available_space + 1
  elif direction == 'right':
    for x in range(1,int(my_length/2)):
      for y in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']+x, my_head['y']-y):
          available_space = available_space + 1
  elif direction == 'down':
    for y in range(1,int(my_length/2)):
      for x in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']+y):
          available_space = available_space + 1
  else:
    for y in range(1,int(my_length/2)):
      for x in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']-y):
          available_space = available_space + 1

  return available_space >= my_length

def has_some_room(data, me, direction):
  available_space = 0

  my_length = len(me['body'])
  my_head = me['body'][0]
  if direction == 'left':
    for x in range(1,int(my_length/2)):
      for y in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']-y):
          available_space = available_space + 1
  elif direction == 'right':
    for x in range(1,int(my_length/2)):
      for y in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']+x, my_head['y']-y):
          available_space = available_space + 1
  elif direction == 'down':
    for y in range(1,int(my_length/2)):
      for x in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']+y):
          available_space = available_space + 1
  else:
    for y in range(1,int(my_length/2)):
      for x in range(int(my_length/2)*-1,int(my_length/2)):
        if is_safe(data, my_head['x']-x, my_head['y']-y):
          available_space = available_space + 1

  return available_space >= int(my_length * .75)

def within_one(body_part, x, y, me):
  for my_body_part in me['body']:
    if my_body_part['x'] == body_part['x'] and my_body_part['y'] == body_part['y']:
      return False

    x_distance = body_part['x'] - x
    y_distance = body_part['y'] - y

    global best_move
    global best_move_distance
    global best_move_coords
    global closest_snake_distance

    if closest_snake_distance == (abs(x_distance) + abs(y_distance)):
      if abs(x_distance) > best_move_distance or abs(y_distance) > best_move_distance:
        if abs(x_distance) > abs(y_distance):
          best_move_distance = abs(x_distance)
          if x_distance > 0:
            best_move = 'left'
            best_move_coords = {
              'x': me['body'][0]['x']-1,
              'y': me['body'][0]['y']
            }
          else:
            best_move = 'right'
            best_move_coords = {
              'x': me['body'][0]['x']+1,
              'y': me['body'][0]['y']
            }
        else:
          best_move_distance = abs(y_distance)
          if y_distance > 0:
            best_move = 'up'
            best_move_coords = {
              'x': me['body'][0]['x'],
              'y': me['body'][0]['y']-1
            }
          else:
            best_move = 'down'
            best_move_coords = {
              'x': me['body'][0]['x'],
              'y': me['body'][0]['y']+1
            }

  return (abs(x_distance) <= 1 and abs(y_distance) <= 1)

def is_safe(data, x, y, check_super_safe=False, check_head_safe=False):
  if x >= data['board']['height'] or y >= data['board']['height'] or x < 0 or y < 0:
    return False

  me = data['you']

  global closest_snake_distance

  for snake in data['board']['snakes']:
    snake_distance = abs(me['body'][0]['x'] - snake['body'][0]['x']) + abs(me['body'][0]['y'] - snake['body'][0]['y'])
    if snake_distance < closest_snake_distance:
      closest_snake_distance = snake_distance

    for body_part in snake['body']:
      if check_super_safe and within_one(body_part, x, y, me) and len(me['body']) <= len(snake['body']):
        return False
      elif check_head_safe and within_one(snake['body'][0], x, y, {'body': [me['body'][0]]}):
        return False
      elif body_part['x'] == x and body_part['y'] == y and (body_part['x'] != snake['body'][0]['x'] or body_part['y'] != snake['body'][0]['y'] or len(me['body']) <= len(snake['body'])):
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

  global best_move
  global best_move_distance
  global best_move_coords
  global closest_snake_distance
  best_move = None
  best_move_distance = 0
  best_move_coords = {
    'x': 0,
    'y': 0
  }
  closest_snake_distance = 1000

  if food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_super_safe=True) and has_room(data, data['you'], 'right'):
    print('*** Super safe food right with room')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_super_safe=True) and has_room(data, data['you'], 'left'):
    print('*** Super safe food left with room')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_super_safe=True) and has_room(data, data['you'], 'down'):
    print('*** Super safe food down with room')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_super_safe=True) and has_room(data, data['you'], 'up'):
    print('*** Super safe food up with room')
    return 'up'
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']) and has_room(data, data['you'], 'right'):
    print('*** Super safe head food right with room')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']) and has_room(data, data['you'], 'left'):
    print('*** Super safe head food left with room')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1) and has_room(data, data['you'], 'down'):
    print('*** Super safe head food down with room')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1) and has_room(data, data['you'], 'up'):
    print('*** Super safe head food up with room')
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_super_safe=True) and has_room(data, data['you'], 'right'):
    print('*** Super safe right with room')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_super_safe=True) and has_room(data, data['you'], 'left'):
    print('*** Super safe left with room')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_super_safe=True) and has_room(data, data['you'], 'down'):
    print('*** Super safe down with room')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_super_safe=True) and has_room(data, data['you'], 'up'):
    print('*** Super safe up with room')
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']) and has_room(data, data['you'], 'right'):
    print('*** Super safe head right with room')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']) and has_room(data, data['you'], 'left'):
    print('*** Super safe head left with room')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1) and has_room(data, data['you'], 'down'):
    print('*** Super safe head down with room')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1) and has_room(data, data['you'], 'up'):
    print('*** Super safe head up with room')
    return 'up'
  elif best_move and is_safe(data, best_move_coords['x'], best_move_coords['y']) and has_room(data, data['you'], best_move):
    print('*** Best move ' + best_move + ' to ' + str(best_move_coords['x']) + ',' + str(best_move_coords['y']) + ' with room')
    return best_move
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_super_safe=True) and has_some_room(data, data['you'], 'right'):
    print('*** Super safe food right with some room')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_super_safe=True) and has_some_room(data, data['you'], 'left'):
    print('*** Super safe food left with some room')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_super_safe=True) and has_some_room(data, data['you'], 'down'):
    print('*** Super safe food down with some room')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_super_safe=True) and has_some_room(data, data['you'], 'up'):
    print('*** Super safe food up with some room')
    return 'up'
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']) and has_some_room(data, data['you'], 'right'):
    print('*** Super safe head food right with some room')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']) and has_some_room(data, data['you'], 'left'):
    print('*** Super safe head food left with some room')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1) and has_some_room(data, data['you'], 'down'):
    print('*** Super safe head food down with some room')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1) and has_some_room(data, data['you'], 'up'):
    print('*** Super safe head food up with some room')
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_super_safe=True) and has_some_room(data, data['you'], 'right'):
    print('*** Super safe right with some room')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_super_safe=True) and has_some_room(data, data['you'], 'left'):
    print('*** Super safe left with some room')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_super_safe=True) and has_some_room(data, data['you'], 'down'):
    print('*** Super safe down with some room')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_super_safe=True) and has_some_room(data, data['you'], 'up'):
    print('*** Super safe up with some room')
    return 'up'
  elif is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']) and has_some_room(data, data['you'], 'right'):
    print('*** Super safe head right with some room')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']) and has_some_room(data, data['you'], 'left'):
    print('*** Super safe head left with some room')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1) and has_some_room(data, data['you'], 'down'):
    print('*** Super safe head down with some room')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1) and has_some_room(data, data['you'], 'up'):
    print('*** Super safe head up with some room')
    return 'up'
  elif best_move and is_safe(data, best_move_coords['x'], best_move_coords['y']) and has_some_room(data, data['you'], best_move):
    print('*** Best move ' + best_move + ' to ' + str(best_move_coords['x']) + ',' + str(best_move_coords['y']) + ' with some room')
    return best_move
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_super_safe=True):
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
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']):
    print('*** Super safe head food right')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']):
    print('*** Super safe head food left')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1):
    print('*** Super safe head food down')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1):
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
  elif is_safe(data, me['x']+1, me['y'], check_head_safe=True) and is_safe(data, me['x']+1, me['y']):
    print('*** Super safe head right')
    return 'right'
  elif is_safe(data, me['x']-1, me['y'], check_head_safe=True) and is_safe(data, me['x']-1, me['y']):
    print('*** Super safe head left')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1, check_head_safe=True) and is_safe(data, me['x'], me['y']+1):
    print('*** Super safe head down')
    return 'down'
  elif is_safe(data, me['x'], me['y']-1, check_head_safe=True) and is_safe(data, me['x'], me['y']-1):
    print('*** Super safe head up')
    return 'up'
  elif best_move and is_safe(data, best_move_coords['x'], best_move_coords['y']):
    print('*** Best move ' + best_move + 'to ' + str(best_move_coords['x']) + ',' + str(best_move_coords['y']))
    return best_move
  elif food and me['x'] < food['x'] and is_safe(data, me['x']+1, me['y']) and has_room(data, data['you'], 'right'):
    print('*** Safe food right with room')
    return 'right'
  elif food and me['x'] > food['x'] and is_safe(data, me['x']-1, me['y']) and has_room(data, data['you'], 'left'):
    print('*** Safe food left with room')
    return 'left'
  elif food and me['y'] < food['y'] and is_safe(data, me['x'], me['y']+1) and has_room(data, data['you'], 'down'):
    print('*** Safe food down with room')
    return 'down'
  elif food and me['y'] > food['y'] and is_safe(data, me['x'], me['y']-1) and has_room(data, data['you'], 'up'):
    print('*** Safe food up with room')
    return 'up'
  elif is_safe(data, me['x']+1, me['y']) and has_room(data, data['you'], 'right'):
    print('*** Safe right with room')
    return 'right'
  elif is_safe(data, me['x']-1, me['y']) and has_room(data, data['you'], 'left'):
    print('*** Safe left with room')
    return 'left'
  elif is_safe(data, me['x'], me['y']+1) and has_room(data, data['you'], 'down'):
    print('*** Safe down with room')
    return 'down'
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
