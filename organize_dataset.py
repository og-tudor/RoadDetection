import os
import json
import shutil
from tqdm import tqdm

def organize_data(split_name, xml_files, images_dir, labels_dir, output_image_dir, output_label_dir):
    """
    Organizes data by copying images and their corresponding labels to the designated directories.

    Parameters:
    - split_name (str): Name of the split ('train' or 'val').
    - xml_files (list): List of XML filenames corresponding to the split.
    - images_dir (str): Source directory containing .jpg and .xml files.
    - labels_dir (str): Source directory containing .txt label files.
    - output_image_dir (str): Destination directory for images.
    - output_label_dir (str): Destination directory for labels.
    """
    print(f"\nProcessing '{split_name}' split...")
    for xml_file in tqdm(xml_files, desc=f"Copying {split_name} data"):
        base_name = os.path.splitext(xml_file)[0]
        
        # Define image file (assuming .jpg extension)
        image_file = f"{base_name}.jpg"
        src_image_path = os.path.join(images_dir, image_file)
        dst_image_path = os.path.join(output_image_dir, image_file)
        
        # Copy image file
        if os.path.exists(src_image_path):
            shutil.copy(src_image_path, dst_image_path)
        else:
            print(f"⚠️ Image file '{image_file}' not found in '{images_dir}'!")
        
        # Define label file (.txt)
        label_file = f"{base_name}.txt"
        src_label_path = os.path.join(labels_dir, label_file)
        dst_label_path = os.path.join(output_label_dir, label_file)
        
        # Copy label file
        if os.path.exists(src_label_path):
            shutil.copy(src_label_path, dst_label_path)
        else:
            print(f"⚠️ Label file '{label_file}' not found in '{labels_dir}'!")

if __name__ == "__main__":
    # Define paths (ensure these paths are correct)
    splits_file = './splits.json'                 # Path to splits.json
    images_dir = './annotated-images'             # Directory containing .jpg and .xml files
    labels_dir = './converted_labels'             # Directory containing .txt files

    # Define output directories
    output_image_dir_train = 'images/train'
    output_image_dir_val = 'images/val'
    output_label_dir_train = 'labels/train'
    output_label_dir_val = 'labels/val'

    # Create output directories if they don't exist
    os.makedirs(output_image_dir_train, exist_ok=True)
    os.makedirs(output_image_dir_val, exist_ok=True)
    os.makedirs(output_label_dir_train, exist_ok=True)
    os.makedirs(output_label_dir_val, exist_ok=True)

    # Load splits.json
    with open(splits_file, 'r') as f:
        splits = json.load(f)

    # Extract training and validation XML filenames
    train_xml_files = splits.get('train', [])
    val_xml_files = splits.get('test', [])  # Assuming 'test' split is intended for validation

    # Organize training data
    organize_data(
        split_name='train',
        xml_files=train_xml_files,
        images_dir=images_dir,
        labels_dir=labels_dir,
        output_image_dir=output_image_dir_train,
        output_label_dir=output_label_dir_train
    )

    # Organize validation data
    organize_data(
        split_name='val',
        xml_files=val_xml_files,
        images_dir=images_dir,
        labels_dir=labels_dir,
        output_image_dir=output_image_dir_val,
        output_label_dir=output_label_dir_val
    )

    print("\n✅ Dataset organization completed successfully!")
