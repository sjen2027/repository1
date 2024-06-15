def task1(key, filename, indicator):
    #TODO
    ''' 
    First, create a list with each element being a string containing two
    letters to be swapped. The list is ordered by the swap order, which
    will be the same order as in the key for encoding, and the reverse
    for decoding.
    '''
    swap_list = []
    k = True
    if indicator == 'e':
      for letter in key:
        if k:
          swap_list.append(letter)
          k = False
        else:
          swap_list[len(swap_list) - 1] += letter
          k = True
    else:
      i = len(key) - 1
      while i >= 0:
        if k:
          swap_list.append(key[i])
          k = False
        else:
          swap_list[len(swap_list) - 1] += key[i]
          k = True
        i -= 1
      '''
      The text is then read into the program and the swaps are applied.
      The output is recorded in the 'output' variable
      '''
    output = ''
    for line in open(filename):
        swapped_line = line
        # for each letter swap, the line is iterated over and the swap applied
        for i in swap_list:
          new_line = ''
          for letter in swapped_line:
            a = letter # letter to be swapped
            if letter.upper() == i[0]:
              if letter.islower():
                a = i[1].lower()
              else:
                a = i[1]
            elif letter.upper() == i[1]:
              if letter.islower():
                a = i[0].lower()
              else:
                a = i[0]
            new_line += a
          swapped_line = new_line
        output += swapped_line
    return output

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task1 function
  print(task1('AE', 'spain.txt', 'd'))
  print(task1('VFSC', 'ai.txt', 'd'))
  print(task1('ABBC', 'cabs_plain.txt', 'e'))