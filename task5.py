def task5(message_filename, is_goal):
    #TODO
    ans = 0
    if is_goal:
      return ans
    search_str = 'ETAONS'
    freq = {'E': 0, 'T': 0, 'A': 0, 'O': 0, 'N': 0, 'S': 0}
    for line in open(message_filename):
      for char in line.rstrip('\n'):
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

if __name__ == '__main__':
  # Example function calls below, you can add your own to test the task5 function
  print(task5('freq_eg1.txt', False))
  print(task5('freq_eg1.txt', True))
  print(task5('freq_eg2.txt', False))
