import os
import librosa
import numpy as np
import random
import pickle
import soundfile as sf
import sounddevice as sd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# ==== PARAMETER ====
SAMPLE_RATE = 16000
DURATION = 2.0
SAMPLES = int(SAMPLE_RATE * DURATION)
MFCC_N = 13
DATA_PATH = 'dataset_augmented'
EPOCHS = 50
LR = 0.01
MODEL_PATH = 'model_cnn_mlp_manual.pkl'

# ==== AKTIVASI ====
def relu(x): return np.maximum(0, x)
def relu_derivative(x): return (x > 0).astype(float)
def softmax(x): return np.exp(x - np.max(x, axis=1, keepdims=True)) / np.sum(np.exp(x - np.max(x, axis=1, keepdims=True)), axis=1, keepdims=True)
def cross_entropy_loss(y_true, y_pred): return -np.sum(y_true * np.log(y_pred + 1e-9)) / y_true.shape[0]

# ==== EKSTRAKSI FITUR ====
def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=SAMPLE_RATE)
    y = librosa.util.fix_length(data=y, size=SAMPLES)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=MFCC_N)  # shape: (n_mfcc, time)
    mfcc = mfcc.T  # shape: (time, n_mfcc)

    # domain waktu & frekuensi
    rms = np.mean(librosa.feature.rms(y=y))
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
    bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
    return mfcc, np.array([rms, zcr, centroid, rolloff, bandwidth])

# ==== LOAD DATA ====
X_mfcc, X_extra, y, file_paths = [], [], [], []
for label in os.listdir(DATA_PATH):
    for fname in os.listdir(os.path.join(DATA_PATH, label)):
        if fname.endswith('.wav'):
            path = os.path.join(DATA_PATH, label, fname)
            mfcc, extra = extract_features(path)
            X_mfcc.append(mfcc)
            X_extra.append(extra)
            y.append(label)
            file_paths.append(path)

# Padding
max_len = max(m.shape[0] for m in X_mfcc)
X_mfcc = np.array([np.pad(m, ((0, max_len - m.shape[0]), (0, 0))) for m in X_mfcc])
X_extra = np.array(X_extra)
X_extra = (X_extra - X_extra.mean(axis=0)) / X_extra.std(axis=0)

# Label encoding
le = LabelEncoder()
y_encoded = le.fit_transform(y)
y_onehot = np.zeros((len(y_encoded), 2))
y_onehot[np.arange(len(y_encoded)), y_encoded] = 1

# Split
X_mfcc_train, X_mfcc_test, \
X_extra_train, X_extra_test, \
y_train, y_test, \
y_train_oh, y_test_oh, \
f_train, f_test = train_test_split(
    X_mfcc, X_extra, y_encoded, y_onehot, file_paths,
    test_size=0.2, stratify=y_encoded, random_state=42
)


# ==== CNN PARAMETER ====
filter_h, filter_w = 3, 3
num_filters = 8
flatten_len = (X_mfcc.shape[1] - filter_h + 1) * (X_mfcc.shape[2] - filter_w + 1) * num_filters
hidden_units = 16

# ==== FUNGSI CONV2D MANUAL ====
def conv2d(x, f):  # x: [H, W], f: [fh, fw]
    h, w = x.shape
    fh, fw = f.shape
    out = np.zeros((h - fh + 1, w - fw + 1))
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            out[i, j] = np.sum(x[i:i+fh, j:j+fw] * f)
    return out

# ==== INIT / LOAD MODEL ====
np.random.seed(42)
if os.path.exists(MODEL_PATH):
    print("📦 Model ditemukan. Melanjutkan ke evaluasi dan prediksi...\n")
    with open(MODEL_PATH, 'rb') as f:
        model_data = pickle.load(f)
    filters = model_data['filters']
    W_mlp = model_data['W_mlp']
    b_mlp = model_data['b_mlp']
    W_out = model_data['W_out']
    b_out = model_data['b_out']

else:
    print("🧠 Melatih model baru...\n")
    filters = np.random.randn(num_filters, filter_h, filter_w) * 0.1
    W_mlp = np.random.randn(X_extra.shape[1], hidden_units) * 0.1
    b_mlp = np.zeros((1, hidden_units))
    W_out = np.random.randn(flatten_len + hidden_units, 2) * 0.1
    b_out = np.zeros((1, 2))

    # ==== TRAINING ====
    for epoch in range(EPOCHS):
        loss_total, correct = 0, 0
        for i in range(len(X_mfcc_train)):
            x_mfcc = X_mfcc_train[i]
            x_extra = X_extra_train[i].reshape(1, -1)
            y_true = y_train_oh[i].reshape(1, -1)

            # CNN forward
            conv_outputs = []
            for f in filters:
                conv_map = conv2d(x_mfcc, f)
                conv_outputs.append(relu(conv_map))
            conv_stack = np.stack(conv_outputs, axis=0)
            flat = conv_stack.reshape(1, -1)

            # MLP forward
            h_mlp = relu(np.dot(x_extra, W_mlp) + b_mlp)

            # Gabungan
            z_concat = np.concatenate([flat, h_mlp], axis=1)
            z_out = np.dot(z_concat, W_out) + b_out
            y_pred = softmax(z_out)

            # Loss dan akurasi
            loss = cross_entropy_loss(y_true, y_pred)
            loss_total += loss
            if np.argmax(y_pred) == np.argmax(y_true):
                correct += 1

            # Backprop
            dL = y_pred - y_true
            dW_out = np.dot(z_concat.T, dL)
            db_out = dL

            dz_concat = np.dot(dL, W_out.T)
            dz_flat = dz_concat[:, :flat.shape[1]]
            dz_mlp = dz_concat[:, flat.shape[1]:]

            dW_mlp = np.dot(x_extra.T, dz_mlp * relu_derivative(h_mlp))
            db_mlp = dz_mlp * relu_derivative(h_mlp)

            # Update
            W_out -= LR * dW_out
            b_out -= LR * db_out
            W_mlp -= LR * dW_mlp
            b_mlp -= LR * db_mlp

        acc = correct / len(X_mfcc_train)
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {loss_total:.4f} - Acc: {acc:.4f}")

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump({
        'filters': filters,
        'W_mlp': W_mlp,
        'b_mlp': b_mlp,
        'W_out': W_out,
        'b_out': b_out
    }, f)
print(f"\n✅ Model berhasil disimpan ke {MODEL_PATH}")



# ==== EVALUASI ====
y_pred = []
for i in range(len(X_mfcc_test)):
    x_mfcc = X_mfcc_test[i]
    x_extra = X_extra_test[i].reshape(1, -1)

    conv_outputs = []
    for f in filters:
        conv_map = conv2d(x_mfcc, f)
        conv_outputs.append(relu(conv_map))
    conv_stack = np.stack(conv_outputs, axis=0)
    flat = conv_stack.reshape(1, -1)

    h_mlp = relu(np.dot(x_extra, W_mlp) + b_mlp)
    z_concat = np.concatenate([flat, h_mlp], axis=1)
    y_out = softmax(np.dot(z_concat, W_out) + b_out)
    y_pred.append(np.argmax(y_out))

# ==== HASIL ====
print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred, target_names=le.classes_))
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=le.classes_)
disp.plot(cmap='Blues')
plt.title("Confusion Matrix")
plt.show()

# ==== PREDIKSI RANDOM ====
idx = random.randint(0, len(X_mfcc_test) - 1)
x_mfcc = X_mfcc_test[idx]
x_extra = X_extra_test[idx].reshape(1, -1)
true = y_test[idx]

conv_outputs = []
for f in filters:
    conv_map = conv2d(x_mfcc, f)
    conv_outputs.append(relu(conv_map))
flat = np.stack(conv_outputs, axis=0).reshape(1, -1)
h_mlp = relu(np.dot(x_extra, W_mlp) + b_mlp)
z_concat = np.concatenate([flat, h_mlp], axis=1)
y_out = softmax(np.dot(z_concat, W_out) + b_out)
pred = np.argmax(y_out)

print(f"\n🎲 File: {f_test[idx]}")
print(f"🎙️  Asli     : {le.inverse_transform([true])[0]}")
print(f"🤖 Prediksi : {le.inverse_transform([pred])[0]} ({np.max(y_out)*100:.2f}%)")

# Play audio
data, sr = sf.read(f_test[idx])
print("🔊 Memutar audio...")
sd.play(data, sr)
sd.wait()
