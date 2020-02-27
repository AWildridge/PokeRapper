import torch
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import torch.nn as nn

from models import ConvNet

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Load the dataset
transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

dataset = torchvision.datasets.ImageFolder("D:/PokeRapper/Pokemon", transform=transform)
dataloader = torch.utils.data.DataLoad(dataset, batch_size=1024, shuffle=True, num_workers=4)

# build the model
# TODO: Add support for loading different models
model = ConvNet()
model.to(device)

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

# train the network
for epoch in range(100):
    for i, data in enumerate(dataloader, 0):
        print('')

