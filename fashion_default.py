import torch
import numpy as np
import torchvision
import os

from norse.torch import LIFParameters
from norse.torch.module.lif import LIFCell
from norse.torch.module.leaky_integrator import LILinearCell
from norse.torch.module import encode
from module_dwmtj_lif import DWMTJCell,DWMTJParameters

from tqdm import tqdm, trange

# folder to save results
target_dir = "240430_fashion_if_2"

BATCH_SIZE = 100

transform = torchvision.transforms.Compose(
    [
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize((0.1307,), (0.3081,)),
    ]
)

train_data = torchvision.datasets.FashionMNIST(
    root=".",
    train=True,
    download=True,
    transform=transform,
)

train_loader = torch.utils.data.DataLoader(
    train_data,
    batch_size=BATCH_SIZE,
    shuffle=True
)

test_loader = torch.utils.data.DataLoader(
    torchvision.datasets.FashionMNIST(
        root=".",
        train=False,
        transform=transform,
    ),
    batch_size=BATCH_SIZE
)

def decode(x):
    x, _ = torch.max(x, 0)
    log_p_y = torch.nn.functional.log_softmax(x, dim=1)
    return log_p_y

class ConvNet(torch.nn.Module):
    def __init__(
        self,  num_channels=1, feature_size=28, method="super", alpha=100
    ):
        super(ConvNet, self).__init__()

        self.features = int(((feature_size - 4) / 2 - 4) / 2)

        self.conv1 = torch.nn.Conv2d(num_channels, 20, 5, 1)
        self.conv2 = torch.nn.Conv2d(20, 50, 5, 1)
        self.fc1 = torch.nn.Linear(self.features * self.features * 50, 500)
        self.lif0 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        self.lif1 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        self.lif2 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        # self.lif0 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        # self.lif1 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        # self.lif2 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        self.out = LILinearCell(500, 10)

    def forward(self, x):
        seq_length = x.shape[0]
        batch_size = x.shape[1]
        
        # specify the initial states
        s0 = s1 = s2 = so = None

        voltages = torch.zeros(
            seq_length, batch_size, 10, device=x.device, dtype=x.dtype
        )

        for ts in range(seq_length):
            z = self.conv1(x[ts, :])
            z, s0 = self.lif0(z, s0)
            z = torch.nn.functional.max_pool2d(z, 2, 2)
            z = 10 * self.conv2(z)
            z, s1 = self.lif1(z, s1)
            z = torch.nn.functional.max_pool2d(z, 2, 2)
            z = z.view(-1, 4 ** 2 * 50)
            z = self.fc1(z)        
            z, s2 = self.lif2(z, s2)
            v, so = self.out(torch.nn.functional.relu(z), so)
            voltages[ts, :, :] = v
        return voltages

class SeqNet(torch.nn.Module):
    def __init__(
        self,  h1=100, h2=100, feature_size=28, beta=20, method="super", alpha=100
    ):
        super(SeqNet, self).__init__()

        self.fc0 = torch.nn.Linear(feature_size*feature_size, h1)
        self.fc1 = torch.nn.Linear(h1, h2)
        self.bn0 = torch.nn.BatchNorm1d(h1)
        self.bn1 = torch.nn.BatchNorm1d(h2)
        self.bnout = torch.nn.BatchNorm1d(10)
        self.lif0 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        self.lif1 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        self.lif2 = LIFCell(p=LIFParameters(method=method, alpha=alpha))
        self.lif0 = LIFCell(p=LIFParameters(method=method, alpha=alpha, tau_syn_inv=50))
        self.lif1 = LIFCell(p=LIFParameters(method=method, alpha=alpha, tau_syn_inv=50))
        self.lif2 = LIFCell(p=LIFParameters(method=method, alpha=alpha, tau_syn_inv=50))
        # self.lif0 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        # self.lif1 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        # self.lif2 = DWMTJCell(p=DWMTJParameters(method=method, alpha=alpha))
        self.out = LILinearCell(h2, 10)

    def forward(self, x):
        seq_length = x.shape[0]
        batch_size = x.shape[1]
        
        # specify the initial states
        s0 = s1 = s2 = so = None

        voltages = torch.zeros(
            seq_length, batch_size, 10, device=x.device, dtype=x.dtype
        )

        for ts in range(seq_length):
            z = self.fc0(x[ts, :].view(-1,28*28))
            z, s0 = self.lif0(z, s0)
            z = self.bn0(z)
            # print(z)
            z = self.fc1(z)
            z, s1 = self.lif1(z, s1)
            z = self.bn1(z)        
            # z = self.bnout(z)
            v, so = self.out(z, so)
            voltages[ts, :, :] = v
        return voltages

class Model(torch.nn.Module):
    def __init__(self, encoder, snn, decoder):
        super(Model, self).__init__()
        self.encoder = encoder
        self.snn = snn
        self.decoder = decoder

    def forward(self, x):
        x = self.encoder(x)
        x = self.snn(x)
        log_p_y = self.decoder(x)
        return log_p_y

def train(model, device, train_loader, optimizer, epoch, max_epochs):
    model.train()
    losses = []
    for (data, target) in tqdm(train_loader, desc='train', unit='batch', ncols=80, leave=False):
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        output = model(data)
        loss = torch.nn.functional.nll_loss(output, target)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    mean_loss = np.mean(losses)
    return losses, mean_loss

def test(model, device, test_loader, epoch):
    model.eval()
    test_loss = 0
    correct = 0
    with torch.no_grad():
        for data, target in tqdm(test_loader, desc='test', unit='batch', ncols=80, leave=False):
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += torch.nn.functional.nll_loss(
                output, target, reduction="sum"
            ).item()  # sum up batch loss
            pred = output.argmax(
                dim=1, keepdim=True
            )  # get the index of the max log-probability
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_loss /= len(test_loader.dataset)
    accuracy = 100.0 * correct / len(test_loader.dataset)
    return test_loss, accuracy

def save(path, epoch, model, optimizer, is_best=False):
    torch.save(
        {
            "epoch": epoch + 1,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
        },
        path,
    )

EPOCHS = 10  
T = 400
LR = 0.001

if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
else:
    DEVICE = torch.device("cpu")

model = Model(
    encoder=encode.ConstantCurrentLIFEncoder(T),
    snn=SeqNet(),
    decoder=decode
).to(DEVICE)

optimizer = torch.optim.Adam(model.parameters(), lr=LR)

training_losses = []
mean_losses = []
test_losses = []
accuracies = []

if not os.path.exists("./outputs/" + target_dir):
    os.mkdir("./outputs/" + target_dir)

pbar = trange(EPOCHS, ncols=80, unit="epoch")
for epoch in pbar:
    training_loss, mean_loss = train(model, DEVICE, train_loader, optimizer, epoch, max_epochs=EPOCHS)
    test_loss, accuracy = test(model, DEVICE, test_loader, epoch)
    training_losses += training_loss
    mean_losses.append(mean_loss)
    test_losses.append(test_loss)
    accuracies.append(accuracy)       
    pbar.set_postfix(accuracy=accuracies[-3:])

    np.save("./outputs/" + target_dir + "/training_losses.npy", np.array(training_losses))
    np.save("./outputs/" + target_dir + "/mean_losses.npy", np.array(mean_losses))
    np.save("./outputs/" + target_dir + "/test_losses.npy", np.array(test_losses))
    np.save("./outputs/" + target_dir + "/accuracies.npy", np.array(accuracies))

model_path = "./outputs/" + target_dir + "/fmnist_dwmtj.pt"
save(
    model_path,
    epoch=epoch,
    model=model,
    optimizer=optimizer,
)

print(f"final accuracy: {accuracies[-1]}")