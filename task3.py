def task3(message_filename, dictionary_filename, threshold):
    #TODO
    # first, load in the words from the dictionary into a list
    dictionary = []
    for word in open(dictionary_filename):
      dictionary.append(word.rstrip('\n'))
    correct = 0
    total = 0
    punct = ",./'!?`~{}[]\"()*&^%$#@<>"
    for line in open(message_filename):
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

if __name__ == '__main__':
    # Example function calls below, you can add your own to test the task3 function
    print(task3('jingle_bells.txt', 'dict_xmas.txt', 90))
    print(task3('fruit_ode.txt', 'dict_fruit.txt', 80))
    print(task3('amazing_poetry.txt', 'common_words.txt', 95))
    