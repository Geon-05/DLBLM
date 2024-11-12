import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array, save_img
from tensorflow.keras.applications import vgg19
import os

# 이미지 크기 설정
img_height = 400
img_width = 400

def preprocess_image(image_path):
    img = load_img(image_path, target_size=(img_height, img_width))
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = vgg19.preprocess_input(img)
    return tf.convert_to_tensor(img, dtype=tf.float32)

def deprocess_image(x):
    x = x.reshape((img_height, img_width, 3))
    x[:, :, 0] += 103.939
    x[:, :, 1] += 116.779
    x[:, :, 2] += 123.68
    x = x[:, :, ::-1]
    return np.clip(x, 0, 255).astype("uint8")

def compute_loss(model, loss_weights, init_image, gram_style_features, content_features):
    style_weight, content_weight = loss_weights
    model_outputs = model(init_image)
    style_output_features = model_outputs[:5]
    content_output_features = model_outputs[5:]

    style_score = 0
    content_score = 0

    weight_per_style_layer = 1.0 / float(len(gram_style_features))
    for target_style, comb_style in zip(gram_style_features, style_output_features):
        # 스타일 손실을 위해 gram_matrix의 출력 형태를 맞춤
        target_shape = target_style.get_shape().as_list()
        gram_comb_style = gram_matrix(comb_style)
        gram_comb_style = tf.reshape(gram_comb_style, target_shape)
        style_score += weight_per_style_layer * tf.reduce_mean(tf.square(gram_comb_style - target_style))

    for target_content, comb_content in zip(content_features, content_output_features):
        content_score += tf.reduce_mean(tf.square(comb_content - target_content))

    style_score *= style_weight
    content_score *= content_weight
    loss = style_score + content_score
    return loss

def gram_matrix(input_tensor):
    channels = int(input_tensor.shape[-1])
    a = tf.reshape(input_tensor, [-1, channels])
    gram = tf.matmul(a, a, transpose_a=True)
    return gram

def get_feature_representations(model, content_path, style_path):
    content_image = preprocess_image(content_path)
    style_image = preprocess_image(style_path)

    style_outputs = model(style_image)
    content_outputs = model(content_image)

    style_features = [gram_matrix(style_layer) for style_layer in style_outputs[:5]]
    content_features = [content_layer for content_layer in content_outputs[5:]]
    return style_features, content_features

def main(refer_img_path, target_img_path):

    refer_img_path = refer_img_path.split('/')[-1]
    target_img_path = target_img_path.split('/')[-1]
    
    print("cwd:", os.getcwd())
    
    cwd = os.path.join(os.getcwd(), "flask_web2")    
            
    style_reference_image_path = cwd + '\\static\\images\\'+ refer_img_path # 'static/images/'+ refer_img_path
    target_image_path = cwd + '\\static\\images\\'+ target_img_path # 'static/images/'+ target_img_path
    
    content_weight = 1e3
    style_weight = 1e-2

    result_prefix = cwd + '\\static\\images\\nst_result'

    model = vgg19.VGG19(include_top=False, weights="imagenet")
    model.trainable = False
    outputs = [model.get_layer(name).output for name in [
        'block1_conv1', 'block2_conv1', 'block3_conv1', 'block4_conv1', 'block5_conv1', 'block5_conv2']]
    model = tf.keras.Model([model.input], outputs)

    style_features, content_features = get_feature_representations(model, target_image_path, style_reference_image_path)
    init_image = tf.Variable(preprocess_image(target_image_path), dtype=tf.float32)

    opt = tf.optimizers.Adam(learning_rate=5.0, beta_1=0.99, epsilon=1e-1)
    best_loss, best_img = float("inf"), None

    loss_weights = (style_weight, content_weight)
    cfg = {
        "model": model,
        "loss_weights": loss_weights,
        "init_image": init_image,
        "gram_style_features": style_features,
        "content_features": content_features
    }

    epochs = 3 #10
    steps_per_epoch = 10 # 100

    for n in range(epochs):
        for m in range(steps_per_epoch):
            with tf.GradientTape() as tape:
                loss = compute_loss(**cfg)
            grads = tape.gradient(loss, init_image)
            opt.apply_gradients([(grads, init_image)])
            if loss < best_loss:
                best_loss = loss
                best_img = deprocess_image(init_image.numpy())
            print(f"Epoch: {n}, Step: {m}, Loss: {loss}")

    save_img(f"{result_prefix}.png", best_img)
    return f"{result_prefix}.png"

if __name__ == "__main__":
    style_reference_image_path = "path/to/style_image.jpg"
    target_image_path = "path/to/target_image.jpg"
    main(style_reference_image_path, target_image_path)
