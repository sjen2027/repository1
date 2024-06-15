import math as m

def gaussian(x, mean, sdev):
  if sdev == 0:
    sdev = 0.001
  ans = (1 / (sdev * m.sqrt(2*m.pi))) * m.exp( -(x-mean)*(x-mean) / (2*sdev*sdev))
  
  if ans < 0.001:
    return 0.001
  return ans

def classify_nb(training_filename, testing_filename):
    # import the training data into a nested list
    x_train = [] # input
    y_train = [] # output
    for line in open(training_filename):
      line_s = line.strip('\n').split(',')     
      label = line_s.pop()
      for i, x in enumerate(line_s):
        line_s[i] = float(x) 
        line_s[i] += 0.0001
      x_train.append(line_s)
      y_train.append(label)   
    # calculate prior probabilities for the training data
    prior = 0 # prior probability of yes
    for i in y_train:
      if i == 'yes':
        prior += 1
    prior /= len(y_train)
    # calculate posterior distribution paramaters for each input variable
    m_post = [] # mean of posterior distribution
    for i in x_train[0]:
      m_post.append([0,0]) # given yes, given no
    sd_post = [] # standard deviation of posterior distribution
    for i in x_train[0]:
      sd_post.append([0,0]) # given yes, given no
    # compute sums
    for i, vector in enumerate(x_train):
      for j, x in enumerate(vector):
        if y_train[i] == 'yes':
          m_post[j][0] += x
        else:
          m_post[j][1] += x
    # take average to compute means
    for i in m_post:
      i[0] /= (len(x_train) * prior)
      i[1] /= (len(x_train) * (1-prior))
    # compute variances
    for i, vector in enumerate(x_train):
      for j, x in enumerate(vector):
        if y_train[i] == 'yes':
          sd_post[j][0] += m.pow((x - m_post[j][0]), 2)
        else:
          sd_post[j][1] += m.pow((x - m_post[j][1]), 2)
    # take average to compute sdev
    for i in sd_post:
      if (len(x_train)*prior - 1) > 0:
        i[0] /= (len(x_train)*prior - 1)
        i[0] = m.sqrt(i[0])
      if (len(x_train)*(1-prior) - 1) > 0:
        i[1] /= (len(x_train)*(1-prior) - 1)
        i[1] = m.sqrt(i[1])
    
    # classify test data
    ans = []
    for line in open(testing_filename):
      data = line.strip('\n').split(',')
      for i, x in enumerate(data):
        data[i] = float(x)
        data[i] += 0.0001
      # calculate probabilities of yes and no
      p_yes = prior
      p_no = 1 - prior
      for i, x in enumerate(data):
        gauss = gaussian(x, m_post[i][0], sd_post[i][0])
        p_yes *= gauss
        gauss = gaussian(x, m_post[i][1], sd_post[i][1])
        p_no *= gauss
      if p_yes >= p_no:
        ans.append('yes')
      else:
        ans.append('no')
    return ans

print(classify_nb('Downloads/training.csv', 'Downloads/test.csv'))