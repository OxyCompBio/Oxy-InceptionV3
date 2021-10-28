import tensorflow as tf
import sys
import os

current_file = os.path.realpath(__file__)
checkpoint_path = os.path.dirname(current_file)
meta_path = sys.argv[1]  # Your .meta file
output_node_names = ['InceptionV3/Predictions/Reshape_1']    # Output nodes
print(checkpoint_path)

with tf.Session() as sess:
    # Restore the graph
    saver = tf.train.import_meta_graph(meta_path)

    # Load weights
    saver.restore(sess,tf.train.latest_checkpoint(checkpoint_path))

    # Freeze the graph
    frozen_graph_def = tf.graph_util.convert_variables_to_constants(
        sess,
        sess.graph_def,
        output_node_names)

    # Save the frozen graph
    with open('output_graph.pb', 'wb') as f:
      f.write(frozen_graph_def.SerializeToString())

