import tensorflow as tf
import numpy as np
import pandas as pd
import glob, os, random

def findTickers(outputfolder):
	tickers = []
	for root, dirs, files in os.walk(outputfolder):
		path = root.split('/')
		#print (len(path) - 1) *'---' , os.path.basename(root)
		for file in files:
			
			

			filename = os.path.join(root, file)
			#print filename
			#print root, dirs, path, file
			#print filename.split("_"), filename

			if ".txt" in file:
				tickers.append(file.split("_")[0].strip('.txt'))
	return tickers

def GetAllCompanies(folder, input_months, output_months):
	X = []
	Y = []
	tickers = findTickers(folder)
	#print tickers
	for ticker in tickers[0:]:
		x, y = GetCompanyData(folder, ticker, input_months, output_months)
		#print x, y
		X += x
		Y += y
	return X, Y


def GetCompanyData(folder, ticker, input_months, output_months):
	X = []
	Y = []
	selected = glob.glob(folder + '/' + ticker + '*.txt')
	df = pd.read_csv(selected[0], error_bad_lines=False, warn_bad_lines=False)
	length = len(df['price']) - (input_months + output_months)
	for i in range(0, length):

		before = np.mean( list(df['price'][i:i+input_months]) )
		after = np.mean( list(df['price'][i+input_months:i+input_months+output_months]) )
		#print before, after
		X.append( list(df['price'][i:i+input_months]) )
		if after/before > 1.6: # 60% uptick
			Y.append( list([1.0 for n in range(0, output_months) ]) )
		elif after/before > 1.4: # 40% uptick
			Y.append( list([0.8 for n in range(0, output_months) ]) )
		elif after/before > 1.1: # 10% uptick
			Y.append( list([0.6 for n in range(0, output_months) ]) )
		else:
			Y.append( list([0.0 for n in range(0, output_months) ]) )
		#print Y
		#print list(df['price'][i+input_months:i+input_months+output_months]), list([1.0 for n in range(0, output_months) ])
		#print type(list(df['price'][i+input_months:i+input_months+output_months])), type(list([1.0 for n in range(0, output_months) ]))
		#raw_input()
	#print len(X), len(Y)
	return X, Y
		

# Neural Network Parameters






N_INPUT_NODES = 8
N_HIDDEN_NODES = 10
N_OUTPUT_NODES  = 1

input_months = N_INPUT_NODES
output_months = N_OUTPUT_NODES
X, Y = GetAllCompanies("normalized", input_months, output_months)
X_test, Y_test = GetAllCompanies("training", input_months, output_months)



N_STEPS = 2000000
N_EPOCH = 5000
ACTIVATION = 'sigmoid' # sigmoid or tanh
COST = 'MSE' # MSE or ACE
LEARNING_RATE = 0.1

N_BATCH = 50
N_TRAINING = N_BATCH





if __name__ == '__main__':


	##############################################################################
	### Create placeholders for variables and define Neural Network structure  ###
	### Feed forward 3 layer, Neural Network.                                  ###
	##############################################################################


	x_ = tf.placeholder(tf.float32, shape=[N_TRAINING, N_INPUT_NODES], name="x-input")
	y_ = tf.placeholder(tf.float32, shape=[N_TRAINING, N_OUTPUT_NODES], name="y-input")

	theta1 = tf.Variable(tf.random_uniform([N_INPUT_NODES,N_HIDDEN_NODES], -1, 1), name="theta1")
	theta2 = tf.Variable(tf.random_uniform([N_HIDDEN_NODES,N_OUTPUT_NODES], -1, 1), name="theta2")

	bias1 = tf.Variable(tf.zeros([N_HIDDEN_NODES]), name="bias1")
	bias2 = tf.Variable(tf.zeros([N_OUTPUT_NODES]), name="bias2")


	if ACTIVATION == 'sigmoid':

		### Use a sigmoidal activation function ###

		layer1 = tf.sigmoid(tf.matmul(x_, theta1) + bias1)
		output = tf.sigmoid(tf.matmul(layer1, theta2) + bias2)

	else:
		### Use tanh activation function ###

		layer1 = tf.tanh(tf.matmul(x_, theta1) + bias1)
		output = tf.tanh(tf.matmul(layer1, theta2) + bias2)
	
		output = tf.add(output, 1)
		output = tf.mul(output, 0.5)

	
	if COST == "MSE":

		# Mean Squared Estimate - the simplist cost function (MSE)

		cost = tf.reduce_mean(tf.square(y_ - output)) 
		train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost)
	
	else:
		# Average Cross Entropy - better behaviour and learning rate

		
		cost = - tf.reduce_mean( (y_ * tf.log(output)) + (1 - y_) * tf.log(1.0 - output)  )
		train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost)


	#train_error = tf.reduce_mean(tf.square(y_ - output))


	init = tf.initialize_all_variables()
	sess = tf.Session()
	sess.run(init)


	for i in range(N_STEPS):
		batch = random.randrange(0, len(X)-N_BATCH)
		sess.run(train_step, feed_dict={x_: X[batch:batch+N_BATCH], y_: Y[batch:batch+N_BATCH]})

		#sess.run(train_error, feed_dict={x_: X, y_: Y})
		#print i, sess.run(train_step)
		#print(sess.eval(train_error))
		#tf.Print(train_error, [train_error])
		#print(train_error)
		if i % N_EPOCH == 0:
			print('Batch: ', i)
			#print('Inference ', sess.run(output, feed_dict={x_: X, y_: Y}))
			print('Cost: ', sess.run(cost, feed_dict={x_: X[0:50], y_: Y[0:50]}))
			#print('Test: ', sess.run(cost, feed_dict={x_: X_test, y_: Y_test}))

			#print('train_error: ', train_error.eval(session=sess))
			#print('train_error: ', sess.run(train_error))

			#tf.Print(train_error, [train_error], message="Training error: ")
					

	#sess.run(cost, feed_dict={x_: X_test, y_: Y_test})


	
