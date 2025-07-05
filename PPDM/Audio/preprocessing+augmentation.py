import os
import librosa
import soundfile as sf
import numpy as np

# === Folder input/output ===
BASE_INPUT = 'dataset_original'
BASE_PREPROCESSED = 'dataset_preprocessed'
BASE_AUGMENTED = 'dataset_augmented'

# Parameter audio
TARGET_SR = 16000
TARGET_DURATION = 2.0  # seconds
SAMPLES = int(TARGET_SR * TARGET_DURATION)

# === Fungsi untuk membuat folder ===
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# === Preprocessing: trim, normalize, pad/crop ===
def preprocess_audio(file_path):
    audio, sr = librosa.load(file_path, sr=TARGET_SR)
    audio, _ = librosa.effects.trim(audio)
    audio = audio / np.max(np.abs(audio))
    if len(audio) < SAMPLES:
        audio = np.pad(audio, (0, SAMPLES - len(audio)))
    else:
        audio = audio[:SAMPLES]
    return audio

# === Augmentasi dasar ===
def augment_audio(audio, sr):
    aug_list = []
    suffixes = []

    # 1. Add noise
    noise = audio + 0.005 * np.random.randn(len(audio))
    aug_list.append(noise)
    suffixes.append('_noise')

    # 2. Pitch shift
    pitch = librosa.effects.pitch_shift(audio, sr=sr, n_steps=2)
    aug_list.append(pitch)
    suffixes.append('_pitch')

    # 3. Time stretch
    stretch = librosa.effects.time_stretch(audio, rate=1.1)
    stretch = librosa.util.fix_length(stretch, size=len(audio))
    aug_list.append(stretch)
    suffixes.append('_stretch')

    # 4. Reverb sederhana (echo dengan decay)
    decay = 0.6
    echo = np.copy(audio)
    for i in range(sr, len(audio)):
        echo[i] += decay * audio[i - sr]  # delay 1 detik
    echo = echo / np.max(np.abs(echo))  # re-normalisasi
    aug_list.append(echo)
    suffixes.append('_reverb')

    # 5. Volume scaling
    volume = audio * 1.5
    volume = np.clip(volume, -1.0, 1.0)
    aug_list.append(volume)
    suffixes.append('_volume')

    return aug_list, suffixes

# === Proses semua file dalam setiap label ===
for label in os.listdir(BASE_INPUT):
    label_dir = os.path.join(BASE_INPUT, label)
    if not os.path.isdir(label_dir):
        continue  # skip file, only process folder

    print(f"\n🔍 Memproses label: {label}")
    out_pre = os.path.join(BASE_PREPROCESSED, label)
    out_aug = os.path.join(BASE_AUGMENTED, label)
    ensure_dir(out_pre)
    ensure_dir(out_aug)

    for fname in os.listdir(label_dir):
        if not fname.endswith('.wav'):
            continue

        in_path = os.path.join(label_dir, fname)

        # === PREPROCESSING ===
        audio = preprocess_audio(in_path)
        sf.write(os.path.join(out_pre, fname), audio, TARGET_SR)

        # === AUGMENTASI ===
        augmented, suffixes = augment_audio(audio, TARGET_SR)
        for aug_audio, suffix in zip(augmented, suffixes):
            new_name = fname.replace('.wav', f'{suffix}.wav')
            sf.write(os.path.join(out_aug, new_name), aug_audio, TARGET_SR)

        print(f"✔ {fname} selesai diproses.")
