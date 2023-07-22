from torchvision.io.image import read_image
from torchvision.models.detection import fasterrcnn_resnet50_fpn_v2, FasterRCNN_ResNet50_FPN_V2_Weights
from torchvision.models import vgg11, VGG11_Weights

from torchvision.utils import draw_bounding_boxes
from torchvision.transforms.functional import to_pil_image

from PIL import Image
import pillow_heif
from pathlib import Path
from PIL import Image
import torch
import torchvision
def classify(input_image): 

    input_name = '.' + input_image.split('.')[1]
    print()

    if(input_image.split('.')[2] != 'jpg'):
        if(input_image.split('.')[2] != 'jpeg'):
            if(input_image.split('.')[2] != 'png'):
                heif_file = pillow_heif.read_heif(input_image)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                )       

                input_image = f"{input_name}.jpg"
                print(input_image)
                image.save(input_image, format="jpeg")
                

    input_image = input_name + '.jpeg'

    my_file = Path(input_image)
    if my_file.is_file():
        custom_image = torchvision.io.read_image(str(input_image))
        custom_image = custom_image / 255
    else:
        input_image = input_name + '.jpg'
        custom_image = torchvision.io.read_image(str(input_image))
        custom_image = custom_image / 255


    

    torch.manual_seed(17)
    data_transform = torchvision.transforms.Compose([
        # Flip the images randomly on the horizontal
        torchvision.transforms.Resize((64, 64)),

        torchvision.transforms.RandomHorizontalFlip(p=0.5), # p = probability of flip, 0.5 = 50% chance
        # Turn the image into a torch.Tensor
        torchvision.transforms.ToTensor() # this also converts all pixel values from 0 to 255 to be between 0.0 and 1.0 
    ])


    testing_data = torchvision.datasets.ImageFolder(root="data_images/imgs", transform=data_transform)

    import torch.nn as nn

    class TinyVGG(nn.Module):
        """
        Model architecture copying TinyVGG
        """
        def __init__(self, input_shape: int, hidden_units: int, output_shape: int) -> None:
            super().__init__()
            self.conv_block_1 = nn.Sequential(
                nn.Conv2d(in_channels=input_shape, 
                        out_channels=hidden_units, 
                        kernel_size=3, # how big is the square that's going over the image?
                        stride=1, # default
                        padding=1), # options = "valid" (no padding) or "same" (output has same shape as input) or int for specific number 
                nn.ReLU(),
                nn.Conv2d(in_channels=hidden_units, 
                        out_channels=hidden_units,
                        kernel_size=3,
                        stride=1,
                        padding=1),
                nn.ReLU(),
                nn.MaxPool2d(kernel_size=2,
                            stride=2) # default stride value is same as kernel_size
            )
            self.conv_block_2 = nn.Sequential(
                nn.Conv2d(hidden_units, hidden_units, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.Conv2d(hidden_units, hidden_units, kernel_size=3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2)
            )
            self.classifier = nn.Sequential(
                nn.Flatten(),
                # Where did this in_features shape come from? 
                # It's because each layer of our network compresses and changes the shape of our inputs data.
                nn.Linear(in_features=hidden_units*16*16,
                        out_features=output_shape)
            )
        
        def forward(self, x: torch.Tensor):
            x = self.conv_block_1(x)
            # print(x.shape)
            x = self.conv_block_2(x)
            # print(x.shape)
            x = self.classifier(x)
            # print(x.shape)
            return x
            # return self.classifier(self.conv_block_2(self.conv_block_1(x))) # <- leverage the benefits of operator fusion

    torch.manual_seed(42)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_0 = TinyVGG(input_shape=3, # number of color channels (3 for RGB) 
                    hidden_units=10, 
                    output_shape=len(testing_data.classes)).to(device)

    model_0.load_state_dict(torch.load(f="model.pth", map_location=torch.device('cpu')))
    #model_0 = model_0.to(device)

    custom_image_transform = torchvision.transforms.Compose([
        torchvision.transforms.Resize((64, 64)),
    ])

    # Transform target image
    custom_image_transformed = custom_image_transform(custom_image)

    model_0.eval()
    with torch.inference_mode():
        # Add an extra dimension to image
        custom_image_transformed_with_batch_size = custom_image_transformed.unsqueeze(dim=0)
        
        # Print out different shapes
        print(f"Custom image transformed shape: {custom_image_transformed.shape}")
        print(f"Unsqueezed custom image shape: {custom_image_transformed_with_batch_size.shape}")
        
        # Make a prediction on image with an extra dimension
        custom_image_pred = model_0(custom_image_transformed.unsqueeze(dim=0).to(device))

    #print(f"Prediction logits: {custom_image_pred}")

    # Convert logits -> prediction probabilities (using torch.softmax() for multi-class classification)
    custom_image_pred_probs = torch.softmax(custom_image_pred, dim=1)
    print(f"Prediction probabilities: {custom_image_pred_probs}")

    # Convert prediction probabilities -> prediction labels
    custom_image_pred_label = torch.argmax(custom_image_pred_probs, dim=1)
    #print(f"Prediction label: {custom_image_pred_label}")
    print(custom_image_pred_label)
    labels = testing_data.classes[custom_image_pred_label]
    
    im = to_pil_image(custom_image_transformed)

    image_name = f"{input_name}-labled.jpg"
    im.save(image_name)

    return image_name, labels

    """ from PIL import Image
    img = Image.open(image_name)
    img.show() """

