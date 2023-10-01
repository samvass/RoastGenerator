import sys
import torch
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import pandas as pd

#input: numpy arr of predicted labels
def get_label_names(bin_label_tensor):
    df = pd.read_csv('../Model/attributes.csv')
    attr_arr = df.columns.values[1:]
    #print(attr_arr)
    attr_indices = torch.nonzero(bin_label_tensor == 1).tolist()
    attr_indices = [x[1] for x in attr_indices]
    print(attr_indices)
    predicted_attributes = [attr_arr[i] for i in attr_indices]
    print(predicted_attributes)

def pre_process_image(img_path):
    image = Image.open(img_path)

    transform = transforms.Compose([transforms.ToTensor()])
    image = transform(image)
    image = image.unsqueeze(0)
    return image

if __name__ == '__main__':
    image_name = sys.argv[1]
    image_path = './images/' + image_name

    # open model
    model = torch.load('../Model/model.pth')

    model.eval()

    # pre process input image
    img = pre_process_image(image_path)

    with torch.no_grad():
        output = model(img).data
        threshold = 0.5
        output_binary = torch.where(output >= threshold, torch.tensor(1), torch.tensor(0))
        
        print(output_binary)
        get_label_names(output_binary)


