def task2(filename, letters):
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
  for swap in swap_list:
    any_swaps = False
    output = ''
    for line in open(filename):
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
  return_str = str(len(string_list))
  for i, output in enumerate(string_list):
    if i == 0:
      return_str += '\n'
    return_str += output
    if i != len(string_list) - 1:
      return_str += '\n\n'
  return return_str
  
if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task2 function
    print(task2('spain.txt', 'ABE'))
    print(task2('ai.txt', 'XZ'))
    print(task2('cabs.txt', 'ABZD'))
    