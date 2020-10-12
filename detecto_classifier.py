
import matplotlib.pyplot as plt
from torchvision import transforms
from detecto.utils import normalize_transform
from detecto.core import Dataset, DataLoader, Model


IMAGE_DIR = '/Users/noahmushkin/codes/selenium-python-scraping/data/images/cameras/'
LABEL_DIR = '/Users/noahmushkin/codes/selenium-python-scraping/data/labeled_cams_convert/'

img_transform = transforms.Compose([
    transforms.ToPILImage(),
    # Note: all images with a size smaller than 800 will be scaled up in size
    transforms.Resize(400),
    transforms.RandomHorizontalFlip(0.5),
    transforms.ColorJitter(saturation=0.2),
    transforms.ToTensor(),  # required
    normalize_transform(),  # required
])

dataset = Dataset(LABEL_DIR, IMAGE_DIR, transform=img_transform)
labels = ['camera']
model = Model(classes=labels)
loader = DataLoader(dataset, batch_size=32, shuffle=True)
losses = model.fit(loader, epochs=10, learning_rate=0.005)
plt.plot(losses)
plt.show()
model.save('cam_model.pth')
