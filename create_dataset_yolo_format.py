import os
import shutil

# Use raw string literals to handle Windows paths
DATA_ALL_DIR = r'C:\Users\karun\Desktop\YoloDataSet\download_folder'
DATA_OUT_DIR = os.path.join('.', 'data')

# Create necessary directories or clear existing ones
for set_ in ['train', 'validation', 'test']:
    for dir_ in [os.path.join(DATA_OUT_DIR, set_),
                 os.path.join(DATA_OUT_DIR, set_, 'imgs'),
                 os.path.join(DATA_OUT_DIR, set_, 'anns')]:
        if os.path.exists(dir_):
            shutil.rmtree(dir_)
        os.makedirs(dir_, exist_ok=True)  # Create directories, including intermediate ones

alpaca_id = '/m/0pcr'

train_bboxes_filename = os.path.join('.', 'oidv6-train-annotations-bbox.csv')
validation_bboxes_filename = os.path.join('.', 'validation-annotations-bbox.csv')
test_bboxes_filename = os.path.join('.', 'test-annotations-bbox.csv')

# Process annotations and filter images
for j, filename in enumerate([train_bboxes_filename, validation_bboxes_filename, test_bboxes_filename]):
    set_ = ['train', 'validation', 'test'][j]
    print(filename)
    with open(filename, 'r') as f:
        line = f.readline()
        while len(line) != 0:
            id, _, class_name, _, x1, x2, y1, y2, _, _, _, _, _ = line.split(',')[:13]
            if class_name in [alpaca_id]:
                src_image_path = os.path.join(DATA_ALL_DIR, '{}.jpg'.format(id))
                dst_image_path = os.path.join(DATA_OUT_DIR, set_, 'imgs', '{}.jpg'.format(id))
                
                if not os.path.exists(dst_image_path):
                    shutil.copy(src_image_path, dst_image_path)
                
                with open(os.path.join(DATA_OUT_DIR, set_, 'anns', '{}.txt'.format(id)), 'a') as f_ann:
                    # class_id, xc, yc, w, h
                    x1, x2, y1, y2 = [float(j) for j in [x1, x2, y1, y2]]
                    xc = (x1 + x2) / 2
                    yc = (y1 + y2) / 2
                    w = x2 - x1
                    h = y2 - y1

                    f_ann.write('0 {} {} {} {}\n'.format(xc, yc, w, h))
            
            line = f.readline()
