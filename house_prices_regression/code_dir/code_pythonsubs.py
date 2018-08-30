import numpy as np
import matplotlib.pylab as plt
import os



#load the data columns show each dimension ndim
#row show a given example of the input training data ndata
#dat = np.loadtxt('pca_fake.dat')
#
#
#
#
#
#
#
#
#
##set k. The number of eigen vectors to consider (MUST be less than Ndim)
#k = 3
##for the plot can give names to each of the axis labels. If empty list then default label
##is dimension 1, 2, 3 etc
#label=[]


def mypca(datin,k,diagfolder='',label=[],meannorm = 1,stdnorm=0): 
 
 if (type(datin) == np.ndarray):
  dat = 1.*datin
 elif (type(a) == str):
  dat = np.loadtxt(datin)
 else:
  raise Exception('Please enter input data datin as a numpy array or a file name containing data')
 
 ndat,ndim = np.shape(dat)
 
 if (k > ndim):
  raise Exception('Must use k < ndim to reduce the dimensionality of the parameter space')
 
 
 
 # do the bit on the data subtract mean and calculate eigen values and eigen vectors.
 # compute the covariance matrix, eigen vectors and eigen values
 if (meannorm == 1):
  mean = np.mean(dat,axis=0)
 else:
  mean = np.mean(dat,axis=0)*0
  
 if (stdnorm == 1):
  std = np.std(dat,axis=0)
 else:
  std = np.std(dat,axis=0)*0 + 1
 
 #subtract the mean
 submean = (dat - mean)/std
 cov  = np.cov(submean.T)
 #compute the eigen values and eigen vectors
 ev = np.linalg.eig(cov)
 eval = ev[0]
 evec = ev[1]
 #generate unit eigen vectors
 uevec = evec/np.sqrt(np.sum(evec**2,axis=1))
 #The proportion of the variance that each eigenvector represents can be 
 #calculated by dividing the eigenvalue corresponding to that eigenvector 
 #by the sum of all eigenvalues.
 evalsum = np.sum(eval)
 fraceval = eval/evalsum
 
 
 
 
 
 
 
 
 #print out the eigen vectors in order of fractional eigen values (large to small)
 idsort = np.argsort(fraceval)[-1::-1]
 for i in range(k):
  idx = idsort[i]
  print 'Eigen vector ',i+1,': ',uevec[:,idx],'.    Fractional variance: ',fraceval[idx]
 
 
 #diagnostic plot only for 2 and 3d
 if (diagfolder != ''):
  os.system('rm -rf '+diagfolder)
  os.system('mkdir '+diagfolder)
  for id1 in range(ndim):
   for id2 in range(ndim):
    if (id1 == id2):
     continue
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(dat[:,id1],dat[:,id2],s=2,color='k',label=None)
    
    xlim = list(ax1.get_xlim())
    xrange = xlim[1]-xlim[0]
    ylim = list(ax1.get_ylim())
    yrange = ylim[1]-ylim[0]
    
    maxrange = np.max([xrange,yrange])
    
    ax1.set_xlim([mean[0]-maxrange,mean[0]+maxrange])
    ax1.set_ylim([mean[1]-maxrange,mean[1]+maxrange])
    if (label == []):
     ax1.set_xlabel('dimension '+np.str(id1))
     ax1.set_ylabel('dimension '+np.str(id2))
    else:
     ax1.set_xlabel(label[id1])
     ax1.set_ylabel(label[id2])
  
    
    #ax1.set_ylim([-plotlim,plotlim])
    #get a line for each eigen vector
    for idx in range(k):
     i = idsort[idx]
     grad  = evec[1,i]/evec[0,i]
     yplot = mean[id2] + grad *(xlim - mean[id1])
     ax1.plot(xlim,yplot,ls='--',label='fractional EV '+np.str(idx+1)+'= '+np.str(np.round(fraceval[i],2)))
     plt.legend()
    #ax1.quiver([0,0],[0,0],[0+evec[0,0],0+evec[0,1]],[0+evec[1,0],0+evec[1,1]])
    plt.savefig(diagfolder+'/fig_'+np.str(id1)+'_'+np.str(id2)+'.pdf')
  
 
  
 #form the data in the k highest prnicpal component frame take transpose at the end to restore
 #the dat[nsamples,ndim] format of the input data
 newdat = np.matmul(evec[:,:].T,submean.T).T
 newdatsort = np.matmul(evec[:,idsort].T,submean.T).T
 
 #plot the data in the principal component space plotting the first principal component on
 #the x axis with y axis of subsequent plots showing the variance across the decresing 
 #eigen vectors 
 if (diagfolder != ''):
  for i in range(1,k):
   fig = plt.figure()
   ax1 = fig.add_subplot(111)
   ax1.scatter(newdatsort[:,0],newdatsort[i],s=2)
   ax1.set_xlabel('EV 1')
   ax1.set_ylabel('EV '+np.str(i+1))
   plt.savefig(diagfolder+'/PCA_'+np.str(i)+'.pdf')
 
 
 return(evec,eval,fraceval,idsort,newdat,newdatsort,mean,std)



#input new definition to make new transformations on new data for eigen values
#already computed
def PCA_convert(dat,evec,meanin=0,stdin=0):
 
 if (meanin > 0):
  mean = 1.*meanin
 elif (meanin == 0):
  mean = 0
 else:
  mean = np.mean(dat,axis=0)
  
 if (stdin > 0):
  std = 1.*stdin
 elif (stdin == 0):
  std = 0
 else:
  std = np.std(dat,axis=0)

 
 
 ndat,ndim = np.shape(dat)
 datsub = np.zeros((ndat,ndim))
 for i in range(ndim):
  datsub[:,i] = (dat[:,i] - mean[i])/std[i]
 newdat = np.matmul(evec[:,:].T,datsub.T).T
 return(newdat) 






import numpy as np
import scipy.stats as sps


def load_train(dim=0,value=0,file=''):

 #either enter file name to load training data or enter manually using dim and value inputs
 if (file != ''):
  dat = np.loadtxt(file)
  dimin = dat[:,:-1]
  valuein = dat[:,-1]
  if (dim == 0 and value == 0):
   raise Exception('must either enter file name or dim and vlaue arrays')
 else:
  dimin = dim
  valuein = value
  
 
 return(dimin,valuein)
 


def k_test(d_test,d_train,v_train,distance=2,k=3):
 
 optest = []
 ntest = np.shape(d_test[:,0])[0]
 ntrain = np.shape(d_train[:,0])[0]
 for i in range(ntest):
  dtest_now = np.repeat(d_test[i,:][np.newaxis],ntrain,axis=0)
  if (distance == 2):#then use euclidean distance
   dist = np.sqrt( np.sum((dtest_now - d_train)**2,axis=1) )
  elif (distance == 1):
   dist = np.sum( np.abs(dtest_now - d_train),axis=1 )
  
  
  #sort the distance into ascending order
  idsort = np.argsort(dist)
  
  #identify the k-nearest neighbours
  d_k = np.array(dist[idsort][:k])
  v_k = np.array(v_train[idsort][:k])
  v_mode = sps.mode(v_k)[0][0]
  
  optest.append(v_mode)
  
 return(optest)
   



#function to implement a k-means clustering algorithm. Test on example free data-sets from 
#UCL machine learning repository https://archive.ics.uci.edu/ml/datasets.html?sort=nameUp&view=list

#UPDATE - How to handle empty clusters? give it a nudge and recompute - doesnt work
# need clever way to choose starting cluster centroid guesses. Assign centroid positions 
# to the positions of the first k points (can also randomly chose which poitns to set as
# the cluster means (LLoyd approach uses assigns random positiomn as cluster centroid - seems shit,
# Mcqueen approach assigns first k data points as cluster centroids - seems to work better
# https://stats.stackexchange.com/questions/89926/what-do-you-do-when-a-centroid-doesnt-attract-any-points-k-means-empty-cluste)



import numpy as np
import matplotlib.pylab as plt
import os
import glob
#x[:ndim,:n] 2-d array of the input n test data in ndim dimensional parameter space
#def kmean(x,k=2,nits=1000,kstart=-1):





##test on fake data
#x = np.loadtxt('make_fake_dim.dat')
#y = np.loadtxt('make_fake_class.dat')
#k=3
#nits=1000
#kstart=-2
#lochange = 0#if lochange or fewer points have switched clusters, 
##the simulation converged and we abort
#diagplot = 1



def kmeans(xin,k=3,nits=1000,lochange=0,kstart=-2,diagplot=0):
 
 #default input has data in first column. This routine requires dimensions to be in first column
 x = xin.T
 
 ndim,ndat = np.shape(x)
 
 smean = np.zeros((ndim,k))
 xmin = np.min(x,axis=1)
 xmax = np.max(x,axis=1)
 xrange = xmax-xmin
 if (kstart == -1):#if -1 then use a guess for the starting means somewhere between the limits of the data 
  for ik in range(k):
   smean[:,ik] = xmin+np.random.rand(ndim)*xrange
   
 elif (kstart == -2): 
  for ik in range(k):
   ikn = np.random.randint(0,ndat,1)[0]
   smean[:,ik] = x[:,ikn]
  
 else:
  smean = kstart 
 
 
 
 idsave = np.zeros((ndat,nits),dtype='int') 
 nksave = np.zeros((k,nits),dtype='int')
 
 
 abort = 0
 it = 0
 
 if (diagplot == 1):
  os.system('rm -rf ./kmeans_testplots')
  os.system('mkdir ./kmeans_testplots')
 
 while (abort == 0 and it < nits):
 #for it in range(nits):#now perform nits iterations of k means clustering or until convergence
  
  #calculate nearest smean to each data point and assign these as cluster
  idnow = np.zeros(ndat)
  for idd in range(ndat):
   xnow = np.repeat(x[:,idd][np.newaxis],k,axis=0).T
   dist = np.sqrt(np.sum((xnow-smean)**2,axis=0))#euclidean distance
   idx  = np.int(np.argmin(dist))
   idnow[idd] = np.int(idx)
   #np.min( 
  
  idsave[:,it] = idnow
  
  #for each cluster compute the mean position in the parameter space and update the 
  #cluster central position
  print 'iteration',it
  changecount = 0
  for ik in range(k):
   id_k = np.where(idnow == ik)[0]
   nk = np.shape(id_k)[0]
   #give a center a random nudge if it has no points assigned
   if (nk == 0):
    smean_new = xmin+np.random.rand(ndim)*xrange
    print 'no points in cluster ',ik,' moving to random position'
   else:
    smean_new = np.mean(x[:,id_k],axis=1)
   
   smean[:,ik] = smean_new
   
   nksave[ik,it] = nk
   #compute how many points have changed groups (should go down as the simulation converges)
   #stop the simulation if the number of points that change groups is less than 'lochange'
   #for idk_now in id_k:
   # print x[:,idk_now]
   #print 'new mean position',smean_new
   if (it > 0):
    nchange = nksave[ik,it]-nksave[ik,it-1] 
    print 'group ',ik,' has',nk,' points. Change=',nchange
    if (lochange >= 0 and nchange <= lochange ):
     changecount = changecount + 1
    if (changecount == k):
     abort = 1
  
  print ''
  print ''
  
  it = it + 1
 
 
 
  #make a diagnostic plot for each iteration if required
  if (diagplot == 1):
   col = ['k','b','r','g']
   fig = plt.figure()
   ax1 = fig.add_subplot(111)
   plot_dim = [0,1]#which two dimensions to show on the scatter plot
   for ik in range(k):
    id_k = np.where(idnow == ik)[0]
    ax1.scatter(x[plot_dim[0],id_k],x[plot_dim[1],id_k],s=2,color=col[ik],label='class '+np.str(ik))
    ax1.plot([smean[0,ik]],[smean[1,ik]],color=col[ik],marker='*',ls='',markersize=15,label=None)
   ax1.set_xlabel('dim '+np.str(plot_dim[0]))
   ax1.set_ylabel('dim '+np.str(plot_dim[1]))
   plt.legend(fontsize='x-small')
   plt.savefig('./kmeans_testplots/testplot_it_'+np.str(it)+'.pdf')
  #for each
 
 
 
 if (diagplot == 1):
  plots = sorted(glob.glob('./kmeans_testplots/testplot_it*.pdf'))
  os.system('open '+plots[0])
  os.system('open '+plots[-1])
 #save the final classifications to an output file
 np.savetxt('km_output.dat',x)
 np.savetxt('km_output_class.dat',idnow)
 np.savetxt('km_output_means.dat',smean)
 
 
 return(smean,idnow)











#with the trained k means algorithm, can now assign new data to a cluster 
def kmeans_predict(yin,smean):

 y = yin.T #again this routine needs dimensions first
 
 ndim,ndat = np.shape(y)
 nk = np.shape(smean)[1]
 idout = np.zeros(ndat)
 for i in range(ndat):
  ynow = np.repeat(y[:,i][np.newaxis],nk,axis=0).T
  dist = np.sqrt(np.sum((ynow-smean)**2,axis=0))#euclidean distance
  idx  = np.int(np.argmin(dist))
  idout[i] = np.int(idx)
 
 return(idout)







#test backpropagating neural network on example data
from random import seed
from random import randrange
from random import random
from csv import reader
from math import exp
import numpy as np 
 
# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset
 
# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())
 
# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = set(class_values)
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup
 
# Find the min and max values for each column
def dataset_minmax(dataset):
	minmax = list()
	stats = [[min(column), max(column)] for column in zip(*dataset)]
	return stats
 
# Rescale dataset columns to the range 0-1
def normalize_dataset(dataset, minmax):
	for row in dataset:
		for i in range(len(row)-1):
			row[i] = (row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0])
 
# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
 
# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
# Evaluate an algorithm using a cross validation split
def evaluate_algorithm(dataset, algorithm, n_folds, *args):
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			row_copy[-1] = None
			
		#print train_set	
		predicted = algorithm(train_set, test_set, *args)
		actual = [row[-1] for row in fold]
		accuracy = accuracy_metric(actual, predicted)
		scores.append(accuracy)
	return scores
 
# Calculate neuron activation for an input
def activate(weights, inputs):
	activation = weights[-1]
	for i in range(len(weights)-1):
		activation += weights[i] * inputs[i]
	return activation
 
# Transfer neuron activation
def transfer(activation):
	return 1.0 / (1.0 + exp(-activation))
 
# Forward propagate input to a network output
def forward_propagate(network, row,diag=0):
 inputs = row
 idxnet = 0
 for layer in network:
  new_inputs = []
  for neuron in layer:
   #print 'length layer ',idxnet,'is',len(layer)
   activation = activate(neuron['weights'], inputs)
   neuron['output'] = transfer(activation)
   new_inputs.append(neuron['output'])
  inputs = new_inputs
  if (diag == 1):
   print 'new inputs level',idxnet,'=',inputs
   print 'new activations',activation
   print 'outputs', transfer(activation)
   idxnet = idxnet + 1
   print 'output is ...',inputs
 return inputs
 
# Calculate the derivative of an neuron output
def transfer_derivative(output):
	return output * (1.0 - output)
 
# Backpropagate error and store in neurons
def backward_propagate_error(network, expected):
	for i in reversed(range(len(network))):
		layer = network[i]
		errors = list()
		if i != len(network)-1:
			for j in range(len(layer)):
				error = 0.0
				for neuron in network[i + 1]:
					error += (neuron['weights'][j] * neuron['delta'])
				errors.append(error)
		else:
			for j in range(len(layer)):
				neuron = layer[j]
				errors.append(expected[j] - neuron['output'])
		for j in range(len(layer)):
			neuron = layer[j]
			neuron['delta'] = errors[j] * transfer_derivative(neuron['output'])
 
# Update network weights with error
def update_weights(network, row, l_rate):
	for i in range(len(network)):
		inputs = row[:-1]
		if i != 0:
			inputs = [neuron['output'] for neuron in network[i - 1]]
		for neuron in network[i]:
			for j in range(len(inputs)):
				neuron['weights'][j] += l_rate * neuron['delta'] * inputs[j]
			neuron['weights'][-1] += l_rate * neuron['delta']
 
# Train a network for a fixed number of epochs
def train_network(network, train, l_rate, n_epoch, n_outputs):
	for epoch in range(n_epoch):
		for row in train:
			outputs = forward_propagate(network, row)
			expected = [0 for i in range(n_outputs)]
			#print 'row',row
			#print 'len row',len(row)
			#print 'row[-1]',row[-1]
			#print 'len expected',len(expected)
			expected[row[-1]] = 1
			backward_propagate_error(network, expected)
			update_weights(network, row, l_rate)
 
# Initialize a network
def initialize_network(n_inputs, n_hidden, n_outputs):
	network = list()
	hidden_layer = [{'weights':[random() for i in range(n_inputs + 1)]} for i in range(n_hidden)]
	network.append(hidden_layer)
	output_layer = [{'weights':[random() for i in range(n_hidden + 1)]} for i in range(n_outputs)]
	network.append(output_layer)
	return network
 
# Make a prediction with a network
def predict(network, row):
	outputs = forward_propagate(network, row)
	return outputs.index(max(outputs))
 
# Backpropagation Algorithm With Stochastic Gradient Descent
def back_propagation(train, test, l_rate, n_epoch, n_hidden):
	n_inputs = len(train[0]) - 1
	n_outputs = len(set([row[-1] for row in train]))
	network = initialize_network(n_inputs, n_hidden, n_outputs)
	train_network(network, train, l_rate, n_epoch, n_outputs)
	predictions = list()
	for row in test:
		prediction = predict(network, row)
		predictions.append(prediction)
	return(predictions)
 



#Custom algorithm modifies above code into a more (imo) intuitive form that accepts numpy 
#arrays

def train_net(traindat,trainclass,l_rate,niterations,n_hidden,normalise = 1):
 ndat,n_inputs = np.shape(traindat)
 n_outputs = np.shape(np.unique(trainclass))[0]
 print n_outputs,np.unique(trainclass),'number of outputs'
 network = initialize_network(n_inputs, n_hidden, n_outputs)
 

 #normalise
 trdat = 1.*traindat
 if (normalise == 1):
  max = np.max(traindat,axis=0)
  min = np.min(traindat,axis=0)
  for i in range(ndat):
   trdat[i,:] = (trdat[i,:] - min)/(max-min)
 
 #convert classes to integers starting at 0
 idclass = np.unique(trainclass)
 nclass = np.shape(idclass)[0]
 idnew = np.arange(nclass)
 idc = []
 for i in range(nclass):
  idnow = idclass[i]
  idc.append(np.where(trainclass == idnow)[0])
 trc = 1.*trainclass
 for i in range(nclass):
  trc[idc[i]] = idnew[i]
 
 ##check 
 #print 'comparing old and new classes'
 #for i in range(ndat):
 # print trc[i],trainclass[i]
 #raw_input()

 #convert to list format
 ds = []
 for i in range(ndat):
  a = [trdat[i,j] for j in range(n_inputs)] + [np.int(trc[i])]
  ds.append(a)
 
 
 train_network(network, ds, l_rate, niterations, n_outputs)
 
 
 #generate key
 idkey = []
 print 'generating key to relate old to new class labels...'
 for i in range(nclass):
  tc_old = trainclass[idc[i]][0]
  tc_new = trc[idc[i]][0]
  idkey.append(tc_old)
  print tc_old,tc_new
 return(network,idkey)


def test_net(testdat,network,idkey=[],normalise=1):
 
 ntest,ndim = np.shape(testdat)
 
 #normalise if this was on for the training it must also be on for testing
 tdat = 1.*testdat
 if (normalise == 1):
  max = np.max(testdat,axis=0)
  min = np.min(testdat,axis=0)
  for i in range(ntest):
   tdat[i,:] = (tdat[i,:] - min)/(max-min)

 
 
 op = []
 for i in range(ntest):
  row = [tdat[i,j] for j in range(ndim)] 
  a = predict(network, row)
  op.append(a)
  
 #relate the class id's in the training to the original values 
 if (idkey != []):
  c_new = []
  classnew = np.unique(op)
  nclass = np.shape(classnew)[0]
  for i in range(ntest):
   i_op = np.int(op[i])
   c_new.append(idkey[i_op])
 else:
  c_new = list(op)
  
 return(op,c_new)




#return the final weifghts of the network as a list of np arrays for plotting with the nn_plot.py code 
def get_weights(network):
 weights=[]
 nlevels = len(network)#length of the network  (excluding the output layer)
 bias = []
 for i in range(nlevels):
  w = network[i]
  nneuron_next = len(w)
  wnow=[]
  bnow = []
  for j in range(nneuron_next):
   wnow.append(w[j]['weights'][:-1])
  wnow = np.array(wnow)
  if (i > 0):
   bnow.append(w[j]['weights'][-1])
  
  weights.append(wnow) 
  bias.append(bnow) 
 return(weights,bias)




## Test Backprop on Seeds dataset
#seed(1)
## load and prepare data
#filename = 'seeds_dataset.csv'
#dataset = load_csv(filename)
#for i in range(len(dataset[0])-1):
#	str_column_to_float(dataset, i)
## convert class column to integers
#str_column_to_int(dataset, len(dataset[0])-1)
## normalize input variables
#minmax = dataset_minmax(dataset)
#normalize_dataset(dataset, minmax)
## evaluate algorithm
#n_folds = 5
#l_rate = 0.3
#n_epoch = 500
#n_hidden = 5
#scores = evaluate_algorithm(dataset, back_propagation, n_folds, l_rate, n_epoch, n_hidden)
#print('Scores: %s' % scores)
#print('Mean Accuracy: %.3f%%' % (sum(scores)/float(len(scores))))
#
#
#
#
#
##now to train the network on your own data
#n_inputs = len(dataset[0])-1
#n_outputs = len(set([row[-1] for row in dataset]))#how many different classifications are there
#network = initialize_network(n_inputs, n_hidden, n_outputs)
#train_network(network, dataset, l_rate, n_epoch, n_outputs)


#filename = 'seeds_dataset.csv'
#l_rate = 0.3
#n_hidden = 5
#datnew = np.genfromtxt(filename, delimiter=',', invalid_raise=False)
#ndat,ndim = np.shape(datnew[:,:-1])
#
#niterations = 500
#ntest = 10
#idtest = np.random.choice(np.arange(ndat), size=ntest, replace=False, p=None)
#
#testdat = datnew[idtest,:-1]
#testclas = datnew[idtest,-1]
#
#
#traindat   = np.delete(datnew[:,:-1],idtest,axis=0)
#trainclass = np.delete(datnew[:,-1],idtest)
#
#
#ntrain = np.shape(trainclass)[0]
#ds = []
#for i in range(ntrain):
# a = [traindat[i,j] for j in range(ndim)] + [np.int(trainclass[i])]
# ds.append(a)
#
#network = train_net(traindat,trainclass,l_rate,niterations,n_hidden)
#op = test_net(testdat,network)
#
#print 'test results'
#for i in range(ntest):
# print testclas[i],op[i]



from matplotlib import pyplot
from math import cos, sin, atan
import numpy as np
import matplotlib as mpl

#make a neural network plot showing the layout of the neural network and the weights as
#lines depending on their weghts
#inputs n_size list with entries containing the number of neurons in each layer 
#the number of layers is the length of the list

#weights is a list of 2d matrices where each element is a (nlayer Xnnext layer) matrix of
#weights between the current layer and the next layer. These are used to set the shading strength of the 
#weight lines between neurons on adjacent levels
#if colorbar = 1 then add on a colour bar with the weights as the coloured axis. 
#If colorbar = -1 then use the line thickness to display the weight parameter
#If colorbar = 0 then plot uniform lines with the same thickness and colour.

#vertical_distance_between_layers = ??,
#horizontal_distance_between_neurons = ??
#These should be configured for each plot to avoid aspect ratio problems or plots
#all squashed into a corner

def makennplot(n_size,weights,vertical_distance_between_layers = 6,
horizontal_distance_between_neurons = 2,
neuron_radius = 0.5,
#number_of_neurons_in_widest_layer = 4,
example=0,color=[],ann_weight=0,alpha=0.5,figtit='nnplot.pdf',ann=[],coan=[],axborder='off',colorbar=1,lwd = -1):


 if (colorbar == 1):
  mymap = mpl.colors.LinearSegmentedColormap.from_list('mycolors',['blue','red'])
  nstep = 10
  weightmin = np.min( np.array([np.min(weights[i]) for i in range(len(weights))]) ) 
  weightmax = np.max( np.array([np.max(weights[i]) for i in range(len(weights))]) ) 
  levels = np.linspace(weightmin,weightmax,nstep)
  Z = [[0,0],[0,0]]
  CS3 = pyplot.contourf(Z,levels,cmap = mymap)
  
 number_of_neurons_in_widest_layer = np.max(np.array(n_size))
 
 class Neuron():
     def __init__(self, x, y, col='r'):
         self.x = x
         self.y = y
         self.color= col
     def draw(self):
         circle = pyplot.Circle((self.x, self.y), radius=neuron_radius, color=self.color,alpha=alpha)
         pyplot.gca().add_patch(circle)
 
 
 class Layer():
     def __init__(self, network, number_of_neurons, weights,col='r'):
         self.color = col
         self.previous_layer = self.__get_previous_layer(network)
         self.y = self.__calculate_layer_y_position()
         self.neurons = self.__intialise_neurons(number_of_neurons)
         self.weights = weights
         
 
     def __intialise_neurons(self, number_of_neurons):
         neurons = []
         x = self.__calculate_left_margin_so_layer_is_centered(number_of_neurons)
         for iteration in range(number_of_neurons):
             neuron = Neuron(x, self.y,col=self.color)
             neurons.append(neuron)
             x += horizontal_distance_between_neurons
         return neurons
 
     def __calculate_left_margin_so_layer_is_centered(self, number_of_neurons):
         return horizontal_distance_between_neurons * (number_of_neurons_in_widest_layer - number_of_neurons) / 2
 
     def __calculate_layer_y_position(self):
         if self.previous_layer:
             return self.previous_layer.y + vertical_distance_between_layers
         else:
             return 0
 
     def __get_previous_layer(self, network):
         if len(network.layers) > 0:
             return network.layers[-1]
         else:
             return None
 
     def __line_between_two_neurons(self, neuron1, neuron2, linewidth, w_ann = ''):
         angle = atan((neuron2.x - neuron1.x) / float(neuron2.y - neuron1.y))
         x_adjustment = neuron_radius * sin(angle)
         y_adjustment = neuron_radius * cos(angle)
         line_x_data = (neuron1.x - x_adjustment, neuron2.x + x_adjustment)
         line_y_data = (neuron1.y - y_adjustment, neuron2.y + y_adjustment)
         if (colorbar == 1):
          r = (float(linewidth) - weightmin)/(weightmax - weightmin)
          g = 0
          b = 1. - r
          
          if (lwd != -1):
           line = pyplot.Line2D(line_x_data, line_y_data,color=(r,g,b),linewidth=lwd)
          else:
           line = pyplot.Line2D(line_x_data, line_y_data,color=(r,g,b))
          
          
          
         elif (colorbar == -1):
          line = pyplot.Line2D(line_x_data, line_y_data, linewidth=linewidth)   
         else:
          if (lwd != -1):
           line = pyplot.Line2D(line_x_data, line_y_data, linewidth = lwd)
          else:
           line = pyplot.Line2D(line_x_data, line_y_data)
          
         pyplot.gca().add_line(line)
         if (w_ann != ''):
          vec12 = np.array( [(neuron2.x - neuron1.x),(neuron2.y - neuron1.y)])
          vecmag = np.sqrt(np.sum(vec12**2))
          #vec21u = vec21/vecmag
          vec1mid = vec12/2.#vecmag/2
          xmid = neuron1.x + vec1mid[0]
          ymid = neuron1.y + vec1mid[1] 
          #print neuron2.x,xmid,neuron1.x
          #print neuron2.y,ymid,neuron1.y
          #print vec21
          #print vec2mid
          #print vecmag 
          pyplot.annotate(np.str(np.round(w_ann,2)),xy=(xmid,ymid),xytext=(xmid,ymid) )
          
     def draw(self):
         for this_layer_neuron_index in range(len(self.neurons)):
             neuron = self.neurons[this_layer_neuron_index]
             neuron.draw()
             if self.previous_layer:
                 for previous_layer_neuron_index in range(len(self.previous_layer.neurons)):
                     previous_layer_neuron = self.previous_layer.neurons[previous_layer_neuron_index]
                     weight = self.previous_layer.weights[this_layer_neuron_index, previous_layer_neuron_index]
                     if (ann_weight != 0):
                      w_ann = weight
                     else:
                      w_ann = ''
                     self.__line_between_two_neurons(neuron, previous_layer_neuron, weight, w_ann=w_ann)
 
 
 class NeuralNetwork():
     def __init__(self):
         self.layers = []
 
     def add_layer(self, number_of_neurons, weights=None,col='k'):
         layer = Layer(self, number_of_neurons, weights,col=col)
         self.layers.append(layer)
 
     def draw(self):
         for layer in self.layers:
             layer.draw()
         pyplot.axis('scaled')
         if (len(ann)>0):
          for ia in range(len(ann)):
           anow = ann[ia]
           conow = coan[ia]
           pyplot.annotate(anow,conow,xycoords='axes fraction')
         if (axborder=='off'):
          for spine in pyplot.gca().spines.values():
           spine.set_visible(False)
          pyplot.tick_params(top='off', bottom='off', left='off', right='off', labelleft='off', labelbottom='off')
         
         if (colorbar == 1):
          cb = pyplot.colorbar(CS3)
          cb.set_label('Weights')
         pyplot.savefig(figtit)
         pyplot.clf()


 if (example == 1):
  number_of_neurons_in_widest_layer = 5
  network = NeuralNetwork()
  # weights to convert from 10 outputs to 4 (decimal digits to their binary representation)
  weights1 = np.array([\
                       [0,0,0,0,0,0,0,0,1,1],\
                       [0,0,0,0,1,1,1,1,0,0],\
                       [0,0,1,1,0,0,1,1,0,0],\
                       [0,1,0,1,0,1,0,1,0,1]]).T
  network.add_layer(4,weights1,col='r')
  network.add_layer(10,col='b') 
  network.draw()
 
 
 
 
 #else then continue to plot the network
 pyplot.clf()
 number_of_neurons_in_widest_layer = np.max(n_size)
 nlayers = np.shape(n_size)[0]
 network = NeuralNetwork()
 idl = 0
 for i in range(nlayers-1,-1,-1):
  if (i-1 < 0):
   network.add_layer(n_size[i],col=color[idl])
   #print i,idl
   #print n_size
   #print weights

  else:
   #print i,idl
   #print n_size
   #print weights
   network.add_layer(n_size[i],weights[i-1],col=color[idl])
  idl = idl + 1
 network.draw()
 
 
 
 return()
 
 
 
#n_size = np.array([60,4,1])
#nlayers = np.shape(n_size)[0]
#weights = [np.random.randn(n_size[i+1],n_size[i]).T for i in range(0,nlayers-1,1)]
#
#a = makennplot(n_size,weights,example=0,color=['k','k','k'],alpha=1.0,lwd=0.1,
#horizontal_distance_between_neurons = 2,
#vertical_distance_between_layers = 50,
#neuron_radius = 1.0)






import numpy as np
import scipy
import scipy.optimize


#ingest set of data find median and uncertainties
#input dat array
# op dmed median of dat, dlo,dup lower and upper sig confidence limits (i.e for 1 sigma, set sig = 0.68)
# disg = (dup-dlo)/2


def stat_uncert(dat,sig=0.68):
 nd = len(dat)#.shape()
 
 dat_sort=np.sort(dat)
 dmed = np.median(dat_sort)
 
 f = (1.-sig/2)
 nup = int(np.ceil((1.-f)*nd))
 nlo = int(np.ceil(f*nd))
 
 
 dlo = dat_sort[nlo]
 dup = dat_sort[nup]
 dsig = np.abs((dup-dlo)/2)
 
 return(dmed,dsig,dlo,dup)
 
 



#return uncertainty in theta give cos(theta) and sig_(costheta)



def sigtheta(costheta, sd_ct):

 ct_mean = np.mean(costheta)
 
 a = np.arccos(ct_mean)
 degmean = 180./np.pi*a
 sdmean =  1./np.sin(a) * sd_ct * 180/np.pi
 
 return(degmean,sdmean)
 
 





# fit polynomial to data by orthogonalizing parameters

#n order of poly
#x,y,sig array of data

def polyfit(x,y,sig,n):
 
 sum1oversig = np.sum(1./sig)
 
 xorth = np.sum(x**n / sig**n) / sum1oversig  
 
 xsuborth = x - xorth
 
 
 
 #fit a nth order poly to xsuborth data
 
 if (n == 1):
  def func(x,a,b): 
   return(a+b*x)
 elif (n==2):
  def func(x,a,b,c):
   return(a+b*x+c*x*x)
 elif (n==3):
  def func(x,a,b,c,d):
   return(a + b*x+c*x*x + d*x*x*x)
 elif (n==4):
  def func(x,a,b,c,d):
   return(a + b*x+c*x*x + d*x*x*x + e*x*x*x*x*x)
 else:
  raise ValueError('This function only works with polynomials up to n=4')
 
 
 
 fit_coef=scipy.optimize.curve_fit(func,np.array(x)-xorth,np.array(y),sigma=np.array(sig))
 sig_coef = np.array(())
 
 for i in range(n+1):
  sig_coef=np.append(sig_coef,np.sqrt([fit_coef[1][i,i]]))
  
 fit_coef = fit_coef[0]
 return(fit_coef,sig_coef,xorth)
  
 
 
 
 

#bayesian information criterion data x, model y,sig, k free params
def bic(x,y,sig,k):
 
 xsuby = x-y
 xsuby2 = xsuby*xsuby
 sig2 = sig*sig
 n=np.shape(x)[0]
 
 chisq = np.sum(xsuby2/sig2)
 
 bic = chisq + k*np.log(n) + n*np.log(2*np.pi) + np.sum(np.log(sig2))
 
 return(bic)
 

 
 
 
#convert uncertainty in  log or cos to real parameter and back again
#convert mean parameter (aveold) and uncertainty sdold and mean both from (1) and to (-1) log par and uncertainty, 
#and from (2) and to (-2) cosine par with uncertainty



def myconvlogsig(iversion,aveold,sdold):


 rln10 = np.log(10.)
 deg2rad = np.pi/180


#if going from log to real
 if (iversion == 1):
  a = 10**aveold
  avenew = a*(1. + 0.5*sdold*sdold*rln10*rln10)
  sdnew  = rln10*a * sdold



 #!! real to log
 elif (iversion == -1):

  a = alog10(aveold)
  avenew = a - 0.5*sdold*sdold/(rln10*aveold*aveold)
  sdnew  = 1./(rln10*aveold) * sdold







#!! cos to real
 elif (iversion ==2):
  print 'mystats doing fuck all'






# real to cos
 elif (iversion == -2):
  print 'mystats doing fuck all'
 
 

 else:
  print 'mystats.f90: iversion',iversion,' is not an option!!'
  exit
  
 
 a = cos(aveold*deg2rad)

 avenew = a*(1. - 0.5*sdold*sdold)
 sdnew  = sin(aveold*deg2rad)*sdold






 return(avenew,sdnew)
 
 
 
 
#function to return the fwhm of a distribution if funny shape just use ends 
def fwhm(t,x):
 xmin = np.min(x)
 xmax = np.max(x) - xmin
 xnew = (x - xmin)/xmax
 idx  = np.where(xnew > 0.5)[0]
 tlo  = t[idx[0]]
 thi  = t[idx[-1]]
 return(thi - tlo)
 
def fwhmall(t,x):
 xmin = np.min(x)
 xmax = np.max(x) - xmin
 xnew = (x - xmin)/xmax
 idx  = np.where(xnew > 0.5)[0]
 tlo  = t[idx[0]]
 thi  = t[idx[-1]]
 return(tlo,thi)
 
 
 
 
 



