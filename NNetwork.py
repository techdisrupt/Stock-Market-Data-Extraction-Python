import tensorflow as tf
import numpy as np
import pandas as pd
import glob, os, random
import matplotlib.pyplot as plt

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
	print tickers
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
		X.append( list(df['price'][i:i+input_months]) + list(df['pe'][i:i+input_months])  )
		"""if after/before > 1.6: # 60% uptick
			Y.append( list([1.0 for n in range(0, output_months) ]) )
		elif after/before > 1.4: # 40% uptick
			Y.append( list([0.8 for n in range(0, output_months) ]) )
		elif after/before > 1.1: # 10% uptick
			Y.append( list([0.6 for n in range(0, output_months) ]) )
		else:
			Y.append( list([0.0 for n in range(0, output_months) ]) )"""

		"""if after/before > 1.3: # 60% uptick
			Y.append( list([1, 0, 0]) )
		elif after/before > 1.2: # 40% uptick
			Y.append( list([0, 1, 0]) )
		elif after/before > 1.1: # 10% uptick
			Y.append( list([0, 0, 1]) )
		else:
			Y.append( list([0, 0, 0 ]) )"""

		if after/before >= 1.20: # 60% uptick
			Y.append( list([0.0, 1.0]) )
		
		else:
			Y.append( list([1.0, 0.0]) )


		#print Y
		#print list(df['price'][i+input_months:i+input_months+output_months]), list([1.0 for n in range(0, output_months) ])
		#print type(list(df['price'][i+input_months:i+input_months+output_months])), type(list([1.0 for n in range(0, output_months) ]))
		#raw_input()
	#print len(X), len(Y)
	return X, Y
		
def ShuffleTrain(X, Y):
	length = len(X)
	
	idx = np.arange(length)
	np.random.shuffle(idx)
	#print length, idx, X
	X_new = [X[i] for i in idx ]
	Y_new = [Y[i] for i in idx ]
	#print Y	
	#print Y_new
	return X_new, Y_new



# Neural Network Parameters






N_INPUT_NODES = 16
N_HIDDEN_NODES = 40
N_OUTPUT_NODES  = 2

input_months = N_INPUT_NODES/2
output_months = 2 # average over X periods
X, Y = GetAllCompanies("normalized", input_months, output_months)
X_test, Y_test = GetAllCompanies("test", input_months, output_months)



N_STEPS = 10000000
N_OUTPUT = 5000
ACTIVATION = 'sigmoid' # sigmoid or tanh
COST = 'MSE' # MSE or ACE
LEARNING_RATE = 0.05
MOMENTUM_RATE = 0.1

N_BATCH = 1000	
N_TRAINING = N_BATCH

TRAIN = True
PLOT = True
CHECK_ACCURACY = True
PREDICT = True
PREDICT_TICKER = None


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
		#train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost)
		#train_step = tf.train.AdagradOptimizer(LEARNING_RATE).minimize(cost)
		#train_step = tf.train.MomentumOptimizer(LEARNING_RATE, MOMENTUM_RATE).minimize(cost)
	
	else:
		# Average Cross Entropy - better behaviour and learning rate

			
		#cost = - tf.reduce_mean( (np.ones(N_OUTPUT_NODES) - y_) * tf.log(np.ones(N_OUTPUT_NODES) - output)  + y_ * tf.log(output)) 
		cost = - tf.reduce_mean( y_ * tf.log(output) + (np.ones(N_OUTPUT_NODES) - y_) * tf.log(np.ones(N_OUTPUT_NODES) - output)  )
		#cost = - tf.reduce_mean( y_ * tf.log(output)   )
		#train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost)

		#tf.reduce_mean(cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(y_, output))
		
	#train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cost)
	train_step = tf.train.MomentumOptimizer(LEARNING_RATE, MOMENTUM_RATE).minimize(cost)




	correct_prediction = tf.equal(tf.argmax(output,1), tf.argmax(y_,1))
	accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
	pred = tf.argmax(output, 1) 


	#train_error = tf.reduce_mean(tf.square(y_ - output))


	init = tf.initialize_all_variables()
	sess = tf.Session()
	sess.run(init)
	saver = tf.train.Saver()

	cost_list = []

	if TRAIN:
		for i in range(N_STEPS):
			batch = random.randrange(0, len(X)-N_BATCH)
			#sess.run(train_step, feed_dict={x_: X[batch:batch+N_BATCH], y_: Y[batch:batch+N_BATCH]})
			X_shuff, Y_shuff = ShuffleTrain(X[batch:batch+N_BATCH], Y[batch:batch+N_BATCH])
			sess.run(train_step, feed_dict={x_: X_shuff, y_: Y_shuff})
			#sess.run(train_error, feed_dict={x_: X, y_: Y})
			#print i, sess.run(train_step)
			#print(sess.eval(train_error))
			#tf.Print(train_error, [train_error])
			#print(train_error)
			if i % N_OUTPUT == 0:
				print('Percentage: ', 100*i/float(N_STEPS))
				print('Batch: ', i)
				#print('Inference ', sess.run(output, feed_dict={x_: X, y_: Y}))
				#print('Cost: ', sess.run(cost, feed_dict={x_: X[batch:batch+N_BATCH], y_: Y[batch:batch+N_BATCH]}))
				#print('Test: ', sess.run(cost, feed_dict={x_: X_test, y_: Y_test}))
				curr_cost = sess.run(cost, feed_dict={x_: X[batch:batch+N_BATCH], y_: Y[batch:batch+N_BATCH]} 	)
				cost_list.append(curr_cost)
				print('cost: ', curr_cost)
				#print('train_error: ', train_error.eval(session=sess))
				#print('train_error: ', sess.run(train_error))

				#tf.Print(train_error, [train_error], message="Training error: ")
					

		save_path = saver.save(sess, "model.ckpt")
	  	print("Model saved in file: %s" % save_path)
	else:
		print("Restoring Model")
		saver.restore(sess, "model.ckpt")

	if PLOT:	
		plt.plot(cost_list)
		plt.show()

	if CHECK_ACCURACY:

		batch_list = []
		for i in range(10000):
			batch = random.randrange(0, len(X_test)-N_BATCH)
			X_shuff_test, Y_shuff_test = ShuffleTrain(X_test[batch:batch+N_BATCH], Y_test[batch:batch+N_BATCH])
			#op = sess.run(output, feed_dict={x_: X_shuff_test, y_: Y_shuff_test})
			batch_accuracy = sess.run(accuracy, feed_dict={x_: X_shuff_test, y_: Y_shuff_test})
			#batch_accuracy = sess.run(accuracy)
			#print('output: ', op)		
			#print('correct_prediction: ',sess.run(correct_prediction, feed_dict={x_: X_test[batch:batch+N_BATCH], y_: Y_test[batch:batch+N_BATCH]}))
			#print('Training: ', batch_accuracy)
			batch_list.append(batch_accuracy)
		print("Mean accuracy: ", np.mean(batch_list))

	if PREDICT:
		con = tf.constant(0.8)
		X_pred = []
		Y_pred = []
		if PREDICT_TICKER != None:

			X_pred_l, Y_pred_l = GetCompanyData('predict', PREDICT_TICKER, input_months, output_months)
			# Predict for the the latest values for company data
			for i in range(0, N_BATCH):
				X_pred.append(X_pred_l[-1])
				Y_pred.append(Y_pred_l[-1])
				# Build the batch
			buy_sell = sess.run(pred, feed_dict={x_: X_pred, y_: Y_pred})
			op = sess.run(output, feed_dict={x_: X_pred, y_: Y_pred})
			print("Prediction: ", op[0])
			print("Buy or Sell: ", buy_sell[0] )
			print(con)
		else:
			tickers = findTickers('predict')
			for ticker in tickers:
				X_pred = []
				Y_pred = []
				X_pred_l, Y_pred_l = GetCompanyData('predict', ticker, input_months, output_months)
				# Predict for the the latest values for company data
				for i in range(0, N_BATCH):
				

					X_pred.append(X_pred_l[-1])
					Y_pred.append(Y_pred_l[-1])
				buy_sell = sess.run(pred, feed_dict={x_: X_pred, y_: Y_pred})
				op = sess.run(output, feed_dict={x_: X_pred, y_: Y_pred})
				print("Ticker: ", ticker)
				print("Prediction: ", op[0])
				print("Buy or Sell: ", buy_sell[0] )
				
				
			
			

		
				



	
