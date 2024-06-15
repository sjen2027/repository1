def classify_nn(training_filename, testing_filename, k):
    # import the training data into a nested list
    x_train = [] # input
    y_train = [] # output
    for line in open(training_filename):
      line_s = line.strip('\n').split(',')     
      label = line_s.pop()
      for i, x in enumerate(line_s):
        line_s[i] = float(x) 
      x_train.append(line_s)
      y_train.append(label)
    # classify test data
    ans = []
    for line in open(testing_filename):
      data = line.strip('\n').split(',')
      for i, x in enumerate(data):
        data[i] = float(x)
      # compute Euclidean distance from each training vector
      dist = []
      for i, vector in enumerate(x_train):
        square_sum = 0
        for j, x in enumerate(data):
          diff = vector[j] - x
          square_sum += diff * diff
        dist.append((square_sum, i))
      sorted_dist = sorted(dist, key=lambda item: item[0])
      # evaluate the class by the nearest neighbours
      i = 0
      nn = []
      while i < k and i < len(x_train):
        nn.append(sorted_dist[i])
        i += 1
      yes_count = 0
      output = 'no'
      for i in nn:
        if y_train[i[1]] == 'yes':
          yes_count += 1
      if yes_count > len(nn) // 2:
        output = 'yes'
      ans.append(output)
    return ans

print(classify_nn('Downloads/training.csv', 'Downloads/test.csv', 4))