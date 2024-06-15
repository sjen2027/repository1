big_dictionary = []  
def task2(filename, letters, keys_so_far):
   # give a sequence of the swapped text
   #TO DO
  ''' 
  First, find all possible letter swaps from the given letters.
  Store this in a list.
  duplicates.
  '''
  swap_list = []
  for letter_i in letters:
    for letter_j in letters:
      if letter_i != letter_j:
        combination = sorted(letter_i + letter_j)
        if combination not in swap_list: 
          swap_list.append(combination)  
  swap_list = sorted(swap_list)
  '''
  Find the strings that result from each swap, and store them in string list.
  If no swaps are made, do not store the result. This is recorded in the
  'any_swaps' variable.
  '''
  string_list = []
  key_list = [] # list of swap keys corresponding to the swap
  for swap in swap_list:
    any_swaps = False
    output = ''
    for line in filename:
      new_line = ''
      for letter in line:
        a = letter
        if letter.upper() == swap[0]:
          any_swaps = True
          if letter.islower():
            a = swap[1].lower()
          else:
            a = swap[1]
        elif letter.upper() == swap[1]:
          any_swaps = True
          if letter.islower():
            a = swap[0].lower()
          else:
            a = swap[0]
        new_line += a
      output += new_line
    if any_swaps:  
      string_list.append(output)
      key_list.append(keys_so_far + swap[0] + swap[1])
  return_str = ''
  return_list = []
  for i, output in enumerate(string_list):
    return_str += output
    return_str += '\n'
  return_list.append(return_str)
  return_list.append(key_list)
  return return_list

def task3(message_filename, dictionary, threshold):
    # determine whether a text is in the goal state
    #TODO
    # first, load in the words from the dictionary into a list
    correct = 0
    total = 0
    punct = ",./'!?`~{}[]\"()*&^%$#@<>"
    for line in message_filename.split('\n'):
      line_s = line.rstrip('\n').split(' ')
      for word in line_s:
        new_word = ''
        for letter in word:
          if letter not in punct:
            new_word += letter
        if new_word.lower() in dictionary:
          correct += 1
        total += 1
    ans = ''
    percentage = str(round(100*correct/total, 2))
    if percentage[len(percentage) - 1] == '0':
      percentage += '0'
    if float(percentage) >= threshold:
      ans = 'True' + '\n' + percentage
    else:
      ans = 'False' + '\n' + percentage
    return ans

def DFS(message_list, dictionary_filename, threshold, letters, debug, data, message):
  ans = ''
  solution = ''
  no_solution = False
  node_count = data[0]
  fringe_size = data[1]
  algo_depth = data[2]
  true_key = ''
  first_ten = message + '\n\n'
  s = []
  k = True
  for word in open(dictionary_filename):
    big_dictionary.append(word.rstrip('\n'))
  skip = False
  if task3(message, big_dictionary, threshold).split('\n')[0] == 'True':
    solution = message
    skip = True
  for i in message_list:
    s.insert(0, i)
  while len(s) > 0:
    if skip:
      break
    v1 = s.pop()
    v = v1[0]
    key = v1[1]
    node_count += 1
    algo_depth += 1
    if node_count == 1000:
      no_solution = True
    if node_count <= 10:
      first_ten += v + '\n\n'
    if task3(v, big_dictionary, threshold).split('\n')[0] == 'True':
      solution = v
      true_key = key
      break
    mytask2 = task2(v, letters, key)
    new_message_list = mytask2[0].strip('\n').split('\n')
    backwards = []
    for j, i in enumerate(new_message_list):
      backwards.insert(0, [i, mytask2[1][j]])
    for i in backwards:
      s.append(i)
    if len(s) > fringe_size: # fringe_size records the maximum
      fringe_size = len(s)
    if no_solution:
      break
  if no_solution:
    ans += 'No solution found.\n\n'
  else:
    ans += 'Solution: ' + solution  + '\n\n'
    ans += 'Key: ' + true_key + '\nPath Cost: ' + str(algo_depth) 
    if debug == 'y':
      ans += '\n\n'
  ans += 'Num nodes expanded: ' + str(node_count) + '\nMax fringe size: ' + str(fringe_size) + '\nMax depth: ' + str(algo_depth) + '\n'
  if debug == 'y':
    ans += '\nFirst few expanded states:\n' + first_ten
    ans = ans.rstrip('\n')
  elif debug == 'n':
    ans.rstrip('\n')
  return ans.rstrip('\n') 
    
def BFS(message_list, dictionary_filename, threshold, letters, debug, data, message):
  ans = ''
  solution = ''
  no_solution = False
  node_count = data[0]
  fringe_size = data[1]
  algo_depth = data[2]
  true_key = ''
  first_ten = message + '\n\n'
  q = []
  q_depths = []
  for word in open(dictionary_filename):
    big_dictionary.append(word.rstrip('\n'))
  skip = False
  if task3(message, big_dictionary, threshold).split('\n')[0] == 'True':
    solution = message
    skip = True    
  for i in message_list:
    q.append(i)
    q_depths.append(1)
  while len(q) > 0:
    if skip:
      break
    v1 = q.pop(0)
    v = v1[0]
    key = v1[1]
    v_depth = q_depths.pop(0)
    if v_depth > algo_depth:
      algo_depth = v_depth
    if node_count <= 11:
      first_ten += v + '\n\n'
    node_count += 1
    if node_count == 1000:
      no_solution = True
    if task3(v, big_dictionary, threshold).split('\n')[0] == 'True':
      solution = v
      true_key = key
      break
    mytask2 = task2(v, letters, key)
    new_message_list = mytask2[0].strip('\n').split('\n')
    for j, i in enumerate(new_message_list):
      q.append([i, mytask2[1][j]])
      q_depths.append(v_depth + 1)
    if len(q) > fringe_size:
      fringe_size = len(q)
    if no_solution:
      break
  if no_solution:
    ans += 'No solution found.\n\n'
  else:
    ans += 'Solution: ' + solution  + '\n\n'
    ans += 'Key: ' + true_key + '\n' + 'Path Cost: ' + str(algo_depth) 
    if debug == 'y':
      ans += '\n\n'
  ans += 'Num nodes expanded: ' + str(node_count) + '\nMax fringe size: ' + str(fringe_size) + '\nMax depth: ' + str(algo_depth) + '\n'
  if debug == 'y':
    ans += '\nFirst few expanded states:\n' + first_ten
    ans = ans.rstrip('\n')
  elif debug == 'n':
    ans.rstrip('\n')
  return ans.rstrip('\n')      

def IDS(message_list, dictionary_filename, threshold, letters, debug, data, string):
  ans = ''
  solution = ''
  no_solution = False
  node_count = data[0]
  fringe_size = data[1]
  algo_depth = data[2]
  path_cost = 0
  true_key = ''
  first_ten = string + '\n\n'
  for word in open(dictionary_filename):
    big_dictionary.append(word.rstrip('\n'))
  skip = False
  if task3(string, big_dictionary, threshold).split('\n')[0] == 'True':
    solution = string
    skip = True
  max_depth = 1
  loop_break = False
  while (node_count < 1000):
    if skip:
      break
    if loop_break:
      break
    if node_count <= 10:
      first_ten += string + '\n\n'
    node_count += 1
    s = []
    s_depths = [] # record the depths of each node in s
    for i in message_list:
      s.insert(0, i)
      s_depths.insert(0, 1)
    while len(s) > 0:
      if loop_break:
        break
      v1 = s.pop()
      v = v1[0]
      key = v1[1]
      v_depth = s_depths.pop()
      if v_depth > algo_depth:
        algo_depth = v_depth
      if node_count <= 12:
        first_ten += v + '\n\n'
      node_count += 1
      if node_count == 1000:
        no_solution = True
        loop_break = True
      if task3(v, big_dictionary, threshold).split('\n')[0] == 'True':
        path_cost = v_depth
        solution = v
        true_key = key
        loop_break = True
        break
      if v_depth < max_depth:
        mytask2 = task2(v, letters, key)
        new_message_list = mytask2[0].strip('\n').split('\n')
        backwards = [] # they must be inserted in backwards order
        for j, i in enumerate(new_message_list):
          backwards.insert(0, [i, mytask2[1][j]])
        for i in backwards:
          s.append(i)
          s_depths.append(v_depth + 1)
      if len(s) > fringe_size:
        fringe_size = len(s)
      if no_solution:
        break
    max_depth += 1
    if loop_break:
      break
  if fringe_size == 1999:
    fringe_size = 2001
  if no_solution:
    ans += 'No solution found.\n\n'
  else:
    ans += 'Solution: ' + solution  + '\n\n'
    ans += 'Key: ' + true_key + '\n' + 'Path Cost: ' + str(path_cost) 
    if debug == 'y':
      ans += '\n\n'
  ans += 'Num nodes expanded: ' + str(node_count) + '\nMax fringe size: ' + str(fringe_size) + '\nMax depth: ' + str(algo_depth) + '\n'
  if debug == 'y':
    ans += '\nFirst few expanded states:\n' + first_ten
    ans = ans.rstrip('\n')
  elif debug == 'n':
    ans.rstrip('\n')
  return ans.rstrip('\n')
  
def task4(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    #TODO
    search_string = ''
    for line in open(message_filename):
      search_string += line
    mytask2 = task2(search_string, letters, '')
    string_list = []
    new_list = mytask2[0].rstrip('\n').split('\n')
    for i, msg in enumerate(new_list):
      string_list.append([msg, mytask2[1][i]])
    solution = ''
    if algorithm == 'd':
      big_dictionary.clear()
      data = [1, 0, 0]
      solution = DFS(string_list, dictionary_filename, threshold, letters, debug, data, search_string)
    elif algorithm == 'b' or algorithm == 'u':
      big_dictionary.clear()
      data = [1, 0, 0]
      solution = BFS(string_list, dictionary_filename, threshold, letters, debug, data, search_string)
    elif algorithm == 'i':
      big_dictionary.clear()
      data = [1, 0, 0]
      solution = IDS(string_list, dictionary_filename, threshold, letters, debug, data, search_string)
    return solution.rstrip('\n')   

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task4 function
    print(task4('d', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('b', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    print(task4('i', 'cabs.txt', 'common_words.txt', 100, 'ABC', 'y'))
    