"""
CNN with 3 conv layers and a fully connected classification layer
PATTERN RECOGNITION EXERCISE:
Fix the three lines below marked with PR_FILL_HERE
"""

import torch.nn as nn


class Flatten(nn.Module):
    """
    Flatten a convolution block into a simple vector.

    Replaces the flattening line (view) often found into forward() methods of networks. This makes it
    easier to navigate the network with introspection
    """
    def forward(self, x):
        x = x.view(x.size()[0], -1)
        return x


class PR_CNN(nn.Module):
    """
    Simple feed forward convolutional neural network

    Attributes
    ----------
    expected_input_size : tuple(int,int)
        Expected input size (width, height)
    conv1 : torch.nn.Sequential
    conv2 : torch.nn.Sequential
    conv3 : torch.nn.Sequential
        Convolutional layers of the network
    fc : torch.nn.Linear
        Final classification fully connected layer

    """

    def __init__(self, **kwargs):
        """
        Creates an CNN_basic model from the scratch.

        Parameters
        ----------
        output_channels : int
            Number of neurons in the last layer
        input_channels : int
            Dimensionality of the input, typically 3 for RGB
        """
        super(PR_CNN, self).__init__()

        # PR_FILL_HERE: Here you have to put the expected input size in terms of width and height of your input image
        self.expected_input_size = (28, 28)

        # self.conv1 = nn.Sequential(
        #     # PR_FILL_HERE: Here you have to put the input channels, output channels ands the kernel size
        #     nn.Conv2d(in_channels=1, out_channels=3, kernel_size=3, stride=3),
        #     nn.LeakyReLU(),

        #     nn.Conv2d(in_channels=3, out_channels=6, kernel_size=3, stride=3),
        #     nn.LeakyReLU(),

        #     nn.Conv2d(in_channels=6, out_channels=6, kernel_size=3, stride=3),
        #     nn.LeakyReLU()
        # )

        # The following configuration works
        # First layer
        self.conv1 = nn.Sequential(
            # PR_FILL_HERE: Here you have to put the input channels, output channels ands the kernel size
            # [(28 - 3) / 3] + 1 = 9 output size 
            # 9 * 9 * 8 = 648 
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3, stride=3),
            nn.LeakyReLU()
        )

        # Second layer
        self.conv2 = nn.Sequential(
            # PR_FILL_HERE: Here you have to put the input channels, output channels ands the kernel size
            # [(9 - 3) / 2] + 1 = 4 output size
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, stride=2),
            nn.LeakyReLU()
        )

        # Third layer
        self.conv3 = nn.Sequential(
            # PR_FILL_HERE: Here you have to put the input channels, output channels ands the kernel size
            # [(4 - 2) / 2] + 1 = 2 output size
            nn.Conv2d(in_channels=16, out_channels=384, kernel_size=2, stride=2),
            nn.LeakyReLU()
        )

        # 1536 = 3 * 2^9 = 6 * 2^8 = 6 * 16 * 16 = 24 * 8 * 8 
        # Number of features = 2 * 2 * 384 = 1536

        # Classification layer
        self.fc = nn.Sequential(
            Flatten(),
            # PR_FILL_HERE: Here you have to put the output size of the linear layer. DO NOT change 1536!
            nn.Linear(1536, 10)
        )

    def forward(self, x):
        """
        Computes forward pass on the network

        Parameters
        ----------
        x : Variable
            Sample to run forward pass on. (input to the model)

        Returns
        -------
        Variable
            Activations of the fully connected layer
        """
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.fc(x)
        return x