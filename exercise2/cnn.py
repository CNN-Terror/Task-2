import model_task2c
import exercise2_config as config
import readers
import torch
import torch.nn.functional as F
import numpy as np

# We first import the data and convert them to a torch version

train_images = readers.ReadFromCsvFile(config.TRAIN_DATA_FILE)
test_images = readers.ReadFromCsvFile(config.TEST_DATA_FILE)

train_data = [image.pixels for image in train_images]
train_labels = [image.label for image in train_images]
test_data = [image.pixels for image in test_images]
test_labels = [image.label for image in test_images]


train_data = np.reshape(train_data, (len(train_data), 1, 28, 28))
train_data = torch.from_numpy(train_data).float()/255
train_labels = torch.from_numpy(np.array(train_labels))
train_set = torch.utils.data.TensorDataset(train_data, train_labels)

test_data = np.reshape(test_data, (len(test_data), 1, 28, 28))
test_data = torch.from_numpy(test_data).float()/255
test_labels = torch.from_numpy(np.array(test_labels))
test_set = torch.utils.data.TensorDataset(test_data, test_labels)


# We have to define a batch size (don't know yet what it is)
batch_size_train = 50
batch_size_test = 1000

# Now we have to build a data loader
train_loader = torch.utils.data.DataLoader(train_set, batch_size = batch_size_train, shuffle = True)
test_loader = torch.utils.data.DataLoader(test_set, batch_size = batch_size_test, shuffle = True)

# Now we can build our model and train it on the train set
# For now we think this should be enough for this function to work
def train(learn_rate, epoch):
    cnn_model = model_task2c.PR_CNN()   # initialization of the model
    cnn_model.train()   # activation of the train mode
    optimizer = torch.optim.SGD(cnn_model.parameters(), lr=learn_rate)

    for index, (data, label) in enumerate(train_loader):
        optimizer.zero_grad()
        output = cnn_model(data)
        loss = F.nll_loss(output, label)
        loss.backward()
        optimizer.step()
    return

# TO DO
def test():
    for index, (data, label) in enumerate(test_loader):

        return

nbr_epochs = 3  # number of time we are going to loop over the train set
learning_rate = 0.01

for epoch in range(1, nbr_epochs + 1):
  train(epoch, learning_rate)
  test()