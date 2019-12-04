import cv2
from src.helpers import *
from src.tf_files.label_map_util import *
from src.tf_files.visualization_utils import *


src_path = get_folder_path()
PATH_TO_CKPT = os.path.join(src_path, 'model', 'frozen_inference_graph.pb')
PATH_TO_LABELS = os.path.join(src_path, 'model', 'labelmap.pbtxt')
NUM_CLASSES = 1

label_map = load_labelmap(PATH_TO_LABELS)
categories = convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

input_files = get_input_files()


def evaluate_input_images():
    for i, input_file in enumerate(input_files):
        image = cv2.imread(os.path.join(get_input_folder_path(), input_file))
        image_expanded = np.expand_dims(image, axis=0)

        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_expanded})

        visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=1,
            min_score_thresh=0.80)

        cv2.imwrite(os.path.join(get_output_folder_path(), input_file), image)
