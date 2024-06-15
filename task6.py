import queue

big_dictionary = {}
punct_str = ",./'!?`~{}[]\"()*&^%$#@<>"
punct = {}
for i in punct_str:
  punct[i] = 0

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
  return_str = []
  return_list = []
  for i, output in enumerate(string_list):
    return_str.append(output)
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
    ans = False
    if 100*correct/total >= threshold:
      ans = True
    return ans
  
def task5(message_filename, is_goal):
    #TODO
    ans = 0
    if is_goal:
      return ans
    search_str = 'ETAONS'
    freq = {'E': 0, 'T': 0, 'A': 0, 'O': 0, 'N': 0, 'S': 0}
    lines = message_filename.split('\n')
    for line in lines:
      for char in line:
        for letter in search_str:
          if char.upper() == letter:
            freq[letter] += 1
    off_count = 0
    new_order = []
    mymax = 0
    max_letter = ''
    new_string = ''
    while(len(freq) > 0):
      mymax = 0
      for letter in freq:
        if freq[letter] >= mymax:
          max_letter = letter 
          mymax = freq[letter]
      new_order.append([max_letter, freq[max_letter]])
      freq.pop(max_letter)
    for i, element1 in enumerate(new_order):
      while True:
        loop_break = True
        for j, element2 in enumerate(new_order):
          if i != j and element2[1] == element1[1] and element2[0] > element1[0]:
            loop_break = False
            temp = element1[0]
            element1[0] = element2[0]
            element2[0] = temp
        if loop_break:
          break 
    for i in new_order:
      new_string += i[0]
    for i, letter in enumerate(new_string):
      if search_str[i] not in letter[0]:
        ans += 1
    ans += 1
    ans = ans // 2
    return ans

def greedy(message_list, dictionary_filename, threshold, letters, debug, data, string):
  ans = ''
  solution = ''
  no_solution = False
  node_count = data[0]
  fringe_size = data[1]
  algo_depth = data[2]
  true_key = ''
  first_ten = string + '\n\n'
  q = queue.PriorityQueue()
  q_depths = queue.PriorityQueue()
  #q.put((6, [string, False]))
  #q_depths.put((6, 0))
  for word in open(dictionary_filename):
    big_dictionary[word.rstrip('\n')] = 0
  message_list = sorted(message_list, key=lambda i: i[1])
  for i in message_list: 
    is_sol = task3(i[0], big_dictionary, threshold)
    mybool = False
    if is_sol == 'True':
      mybool = True
    print(i[0])
    q.put((task5(i[0], is_sol), [i, is_sol]))
    q_depths.put((task5(i[0], is_sol), 1))
  while q.qsize() > 0:
    V = q.get()
    v = V[1][0][0]
    mybool = V[1][1]
    key = V[1][0][1]
    v_depth = q_depths.get()[1]
    if v_depth > algo_depth:
      algo_depth = v_depth
    if node_count <= 11:
      first_ten += v + '\n\n'
    node_count += 1
    if node_count == 1000:
      no_solution = True
    if mybool:
      solution = v
      true_key = key
      break
    mytask2 = task2(v, letters, key)
    new_message_list = mytask2[0]
    new_message_list = sorted(new_message_list, key = lambda i: i[1])
    for j, i in enumerate(new_message_list):
      is_sol =  task3(i, big_dictionary, threshold)
      mybool = False
      if is_sol:
        mybool = True
      q.put((task5(i, is_sol), [[i, mytask2[1][j]], is_sol]))
      q_depths.put((task5(i, is_sol), v_depth + 1))
    if q.qsize() > fringe_size:
      fringe_size = q.qsize()
    if no_solution:
      break
  if no_solution:
    ans += 'No solution found.\n\n'
  else:
    ans += 'Solution: ' + solution  + '\n\n'
    ans += 'Key: ' + true_key + '\n' + 'Path Cost: ' + str(algo_depth) + '\n\n'
  ans += 'Num nodes expanded: ' + str(node_count) + '\nMax fringe size: ' + str(fringe_size) + '\nMax depth: ' + str(algo_depth) + '\n'
  if debug == 'y':
    ans += '\nFirst few expanded states:\n' + first_ten
    ans = ans.rstrip('\n')
  elif debug == 'n':
    ans.rstrip('\n')
  return ans.rstrip('\n')

def a_star(message_list, dictionary_filename, threshold, letters, debug, data, string):
  ans = ''
  solution = ''
  no_solution = False
  node_count = data[0]
  fringe_size = data[1]
  algo_depth = data[2]
  true_key = ''
  first_ten = string + '\n\n'
  q = queue.PriorityQueue()
  q_depths = queue.PriorityQueue()
  #q.put((6, [string, False]))
  #q_depths.put((6, 0))
  for word in open(dictionary_filename):
    big_dictionary[word.rstrip('\n')] = 0
  message_list = sorted(message_list, key=lambda i: i[1])
  for i in message_list:
    is_sol = task3(i[0], big_dictionary, threshold)
    mybool = False
    if is_sol == 'True':
      mybool = True
    q.put((task5(i[0], is_sol), [i, is_sol]))
    q_depths.put((task5(i[0], is_sol), 1))
  while q.qsize() > 0:
    V = q.get()
    v = V[1][0][0]
    mybool = V[1][1]
    key = V[1][0][1]
    v_depth = q_depths.get()[1]
    if v_depth > algo_depth:
      algo_depth = v_depth
    if node_count <= 11:
      first_ten += v + '\n\n'
    node_count += 1
    if node_count == 1000:
      no_solution = True
    if mybool:
      solution = v
      true_key = key
      break
    mytask2 = task2(v, letters, key)
    new_message_list = mytask2[0]
    new_message_list = sorted(new_message_list, key = lambda i: i[1])
    for j, i in enumerate(new_message_list):
      is_sol =  task3(i, big_dictionary, threshold)
      mybool = False
      if is_sol:
        mybool = True
      q.put((task5(i, is_sol) + v_depth + 1, [[i, mytask2[1][j]], is_sol]))
      q_depths.put((task5(i, is_sol) + v_depth + 1, v_depth + 1))
    if q.qsize() > fringe_size:
      fringe_size = q.qsize()
    if no_solution:
      break
  if no_solution:
    ans += 'No solution found.\n\n'
  else:
    ans += 'Solution: ' + solution  + '\n\n'
    ans += 'Key: ' + true_key + '\n' + 'Path Cost: ' + str(algo_depth) + '\n\n'
  ans += 'Num nodes expanded: ' + str(node_count) + '\nMax fringe size: ' + str(fringe_size) + '\nMax depth: ' + str(algo_depth) + '\n'
  if debug == 'y':
    ans += '\nFirst few expanded states:\n' + first_ten
    ans = ans.rstrip('\n')
  elif debug == 'n':
    ans.rstrip('\n')
  return ans.rstrip('\n')


def task6(algorithm, message_filename, dictionary_filename, threshold, letters, debug):
    #TODO
    search_string = ''
    for line in open(message_filename):
      search_string += line
    mytask2 = task2(search_string, letters, '')
    string_list = []
    new_list = mytask2[0]
    for i, msg in enumerate(new_list):
      string_list.append([msg, mytask2[1][i]])
    solution = ''
    if algorithm == 'g':
      big_dictionary.clear()
      data = [1, 0, 0]
      solution = greedy(string_list, dictionary_filename, threshold, letters, debug, data, search_string)
    if algorithm == 'a':
      big_dictionary.clear()
      data = [1, 0, 0]
      solution = a_star(string_list, dictionary_filename, threshold, letters, debug, data, search_string)
    return solution

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task6 function
    print(task6('g', 'secret_msg.txt', 'common_words.txt', 90, 'AENOST', 'n'))
