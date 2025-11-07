import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
import sounddevice as sd

# --- Fenêtre principale ---
root = tk.Tk()
root.title("Égaliseur Audio Fonctionnel 🎚️")
root.geometry("700x600")
root.resizable(False, False)

# --- Variables globales ---
fichier_audio = tk.StringVar(value="Aucun fichier sélectionné")
audio_data = None
fs = None

# --- Fonctions DSP ---
def butter_bandpass(lowcut, highcut, fs, order=8):
    """Crée un filtre passe-bande Butterworth"""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    return butter(order, [low, high], btype='band', output='sos')

def db_to_gain(db):
    """Convertit un gain dB en facteur linéaire"""
    return 10 ** (db / 20)

# --- Sélection du fichier ---
def selectionner_fichier():
    global audio_data, fs
    fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier WAV",
        filetypes=[("Fichiers WAV", "*.wav")]
    )
    if fichier:
        fs, data = wavfile.read(fichier)
        if data.ndim > 1:
            data = data.mean(axis=1)  # stéréo → mono
        audio_data = data.astype(np.float32)
        fichier_audio.set(fichier)
        messagebox.showinfo("Chargement réussi", "Fichier audio chargé avec succès ✅")

# --- Lecture avec égaliseur ---
def lire_audio():
    global audio_data, fs
    if audio_data is None:
        messagebox.showwarning("Attention", "Veuillez d'abord sélectionner un fichier WAV.")
        return

    gains = [float(slider.get()) for slider in sliders]
    bandes = [
        (100, 400),     # Bande 1
        (400, 1000),    # Bande 2
        (1000, 2000),   # Bande 3
        (2000, 4000),   # Bande 4
        (4000, 6000),   # Bande 5
        (6000, 10000),  # Bande 6
    ]

    sortie = np.zeros_like(audio_data)
    for i, (low, high) in enumerate(bandes):
        sos = butter_bandpass(low, high, fs)
        filtré = sosfilt(sos, audio_data)
        gain_lin = db_to_gain(gains[i])
        sortie += filtré * gain_lin

    # Normalisation
    sortie = sortie / np.max(np.abs(sortie))
    sortie = sortie.astype(np.float32)

    print("Lecture du son traité...")
    sd.play(sortie, fs)

# --- Sauvegarde du son traité ---
def enregistrer_audio():
    global audio_data, fs
    if audio_data is None:
        messagebox.showwarning("Attention", "Aucun fichier à enregistrer.")
        return

    gains = [float(slider.get()) for slider in sliders]
    bandes = [
        (100, 400), (400, 1000), (1000, 2000),
        (2000, 4000), (4000, 6000), (6000, 10000)
    ]

    sortie = np.zeros_like(audio_data)
    for i, (low, high) in enumerate(bandes):
        sos = butter_bandpass(low, high, fs)
        filtré = sosfilt(sos, audio_data)
        gain_lin = db_to_gain(gains[i])
        sortie += filtré * gain_lin

    sortie = sortie / np.max(np.abs(sortie))
    wavfile.write("audio_modifie.wav", fs, np.int16(sortie * 32767))
    messagebox.showinfo("Enregistré", "✅ Fichier traité enregistré : audio_modifie.wav")

# --- Interface Tkinter ---
ttk.Label(root, text="🎵 ÉGALISEUR AUDIO (500 Hz → 10 kHz)", font=("Segoe UI", 14, "bold")).pack(pady=10)

btn_fichier = ttk.Button(root, text="🎧 Sélectionner un fichier WAV", command=selectionner_fichier)
btn_fichier.pack(pady=5)

label_fichier = ttk.Label(root, textvariable=fichier_audio, wraplength=650)
label_fichier.pack(pady=5)

frame_sliders = ttk.Frame(root)
frame_sliders.pack(pady=20)

frequences = ["100-400", "400-1k", "1k-2k", "2k-4k", "4k-6k", "6k-10k"]
sliders = []
labels_valeurs = []

for i, freq in enumerate(frequences):
    frame = ttk.Frame(frame_sliders)
    frame.grid(row=0, column=i, padx=10)
    
    slider = ttk.Scale(
        frame,
        from_=20, to=-20,  # +/- 20 dB
        orient='vertical',
        length=250,
        command=lambda val, idx=i: labels_valeurs[idx].config(text=f"{float(val):.1f} dB")
    )
    slider.set(0)
    slider.pack()
    sliders.append(slider)
    
    ttk.Label(frame, text=freq + " Hz").pack()
    lbl_val = ttk.Label(frame, text="0.0 dB")
    lbl_val.pack()
    labels_valeurs.append(lbl_val)

# --- Boutons de contrôle ---
frame_btn = ttk.Frame(root)
frame_btn.pack(pady=15)

ttk.Button(frame_btn, text="Lire avec égaliseur", command=lire_audio).grid(row=0, column=0, padx=10)
ttk.Button(frame_btn, text="Enregistrer le fichier modifié", command=enregistrer_audio).grid(row=0, column=1, padx=10)
ttk.Button(frame_btn, text="Stop", command=lambda: sd.stop()).grid(row=0, column=2, padx=10)

root.mainloop()
