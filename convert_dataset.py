import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
import json

def convert_bbox(size, box):
    dw = 1.0 / size[0]
    dh = 1.0 / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_annotation(xml_folder, output_folder, class_mapping):
    for xml_file in tqdm(os.listdir(xml_folder)):
        if not xml_file.endswith('.xml'):
            continue
        in_file = os.path.join(xml_folder, xml_file)
        tree = ET.parse(in_file)
        root = tree.getroot()
        image_path = root.find('filename').text
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        # Create corresponding txt file
        txt_file = os.path.join(output_folder, xml_file.replace('.xml', '.txt'))
        with open(txt_file, 'w') as out_f:
            for obj in root.iter('object'):
                cls = obj.find('name').text
                if cls not in class_mapping:
                    continue
                cls_id = class_mapping[cls]
                xmlbox = obj.find('bndbox')
                b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                     float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                bb = convert_bbox((w, h), b)
                out_f.write(" ".join([str(a) for a in [cls_id] + list(bb)]) + '\n')

if __name__ == "__main__":
    # Paths (modify these paths according to your dataset location)
    dataset_dir = './annotated-images'  # Replace with your actual path
    splits_file = './splits.json'       # Replace with your actual path
    output_dir = './converted_labels'

    # check if input folder exists
    if not os.path.exists(dataset_dir):
        print("Dataset folder does not exist!")
        exit()
    if not os.path.exists(splits_file):
        print("Splits file does not exist!")
        exit()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define class mapping
    class_mapping = {
        'pothole': 0  # Assuming 'pothole' is the only class
    }

    convert_annotation(dataset_dir, output_dir, class_mapping)
    print("Conversion Completed!")
