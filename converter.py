import os
import cv2
import numpy as np
import torch
from tqdm import tqdm
import subprocess
import zipfile
import json

# Globale Konfiguration
config = {
    "frame_width": 1920,
    "frame_height": 1080,
    "block_size": 10,
    "fps": 30,
    "error_correction_bits": 8,
    "use_gpu": True,  # GPU verwenden
}

# GPU-Gerät konfigurieren
device = torch.device("mps") if config["use_gpu"] and torch.backends.mps.is_available() else "cpu"
print(f"Verwende Gerät: {device}")

def compress_file(input_path, zip_file):
    """Komprimiert eine Datei oder einen Ordner in eine ZIP-Datei."""
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if os.path.isdir(input_path):
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, input_path))
        else:
            zipf.write(input_path, os.path.basename(input_path))
    print(f"Datei {input_path} wurde erfolgreich komprimiert.")

def decompress_file(zip_file, output_folder):
    """Entpackt die ZIP-Datei."""
    with zipfile.ZipFile(zip_file, 'r') as zipf:
        zipf.extractall(output_folder)
    extracted_files = zipf.namelist()
    print(f"ZIP-Datei {zip_file} wurde nach {output_folder} entpackt.")
    return extracted_files

def get_file_metadata(file_path):
    """Liest Erstellungs- und Änderungsdatum der Datei."""
    creation_time = os.path.getctime(file_path)
    modification_time = os.path.getmtime(file_path)
    return {"creation_time": creation_time, "modification_time": modification_time}

def set_file_metadata(file_path, metadata):
    """Setzt Erstellungs- und Änderungsdatum der Datei."""
    os.utime(file_path, (metadata["creation_time"], metadata["modification_time"]))

def create_frame_gpu(frame_idx, bits, bits_per_frame, frame_width, frame_height, block_size):
    """Erstellt Frames auf der GPU."""
    frame_bits = torch.tensor(
        [int(bit) for bit in bits[frame_idx * bits_per_frame:(frame_idx + 1) * bits_per_frame]],
        dtype=torch.uint8,
        device=device
    )
    if frame_bits.size(0) < bits_per_frame:
        frame_bits = torch.nn.functional.pad(frame_bits, (0, bits_per_frame - frame_bits.size(0)))

    frame_bits = frame_bits.reshape((frame_height // block_size, frame_width // block_size))
    frame = frame_bits.repeat_interleave(block_size, dim=0).repeat_interleave(block_size, dim=1) * 255
    return frame.cpu().numpy()

def extract_frame_bits_gpu(frame, frame_width, frame_height, block_size):
    """Extrahiert Bits aus Frames auf der GPU."""
    frame_tensor = torch.tensor(frame, dtype=torch.float32, device=device)
    frame_tensor = frame_tensor.unfold(0, block_size, block_size).unfold(1, block_size, block_size)
    avg_colors = frame_tensor.mean(dim=(-1, -2))
    bits = (avg_colors > 127).flatten().int().tolist()
    return bits

def file_to_bw_video():
    """Konvertiert eine Datei in ein Schwarz-Weiß-Video mit eingebetteten Metadaten."""
    input_file = input("Gib den Pfad zur gewünschten Datei ein: ").strip()
    output_video = input("Gib den Pfad zum Ausgabevideo ein (ohne .mov): ").strip()

    # Metadaten der Datei lesen
    metadata = get_file_metadata(input_file)

    zip_file = input_file + ".zip"
    compress_file(input_file, zip_file)

    with open(zip_file, 'rb') as f:
        data = f.read()

    # JSON-Metadaten hinzufügen
    metadata_json = json.dumps(metadata).encode('utf-8')
    data = metadata_json + b'\n' + data

    bits_with_error_correction = []
    for byte in data:
        data_bits = f'{byte:08b}'
        error_bits = f'{(sum(map(int, data_bits)) % 256):08b}'
        bits_with_error_correction.append(data_bits + error_bits)
    bits = ''.join(bits_with_error_correction)

    frame_width, frame_height, block_size = config["frame_width"], config["frame_height"], config["block_size"]
    bits_per_frame = (frame_width // block_size) * (frame_height // block_size)
    total_frames = (len(bits) + bits_per_frame - 1) // bits_per_frame

    ffmpeg_process = subprocess.Popen(
        [
            "ffmpeg", "-f", "image2pipe", "-framerate", str(config["fps"]), "-i", "-",
            "-c:v", "h264_videotoolbox", "-b:v", "2M", f"{output_video}.mov"
        ],
        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    with tqdm(total=total_frames, desc="Erstelle Frames", unit="frame") as progress:
        for frame_idx in range(total_frames):
            frame = create_frame_gpu(frame_idx, bits, bits_per_frame, frame_width, frame_height, block_size)
            is_success, buffer = cv2.imencode(".png", frame)
            if not is_success:
                raise RuntimeError("Fehler beim Kodieren des Frames.")
            ffmpeg_process.stdin.write(buffer.tobytes())
            progress.update(1)

    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()
    os.remove(zip_file)
    print(f"Video gespeichert unter: {output_video}.mov")

def video_to_file():
    """Konvertiert ein Video zurück in die ursprüngliche Datei und stellt Metadaten wieder her."""
    input_video = input("Gib den Pfad zum Video ein: ").strip()
    output_file = input("Gib den Pfad zur Ausgabedatei ein: ").strip()

    ffmpeg_process = subprocess.Popen(
        [
            "ffmpeg", "-i", input_video, "-f", "rawvideo", "-pix_fmt", "gray", "pipe:"
        ],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
    )

    frame_width, frame_height, block_size = config["frame_width"], config["frame_height"], config["block_size"]
    bits = ""
    frame_size = frame_width * frame_height

    try:
        with tqdm(desc="Lese Frames", unit="frame") as progress:
            while True:
                raw_frame = ffmpeg_process.stdout.read(frame_size)
                if not raw_frame:
                    break

                frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((frame_height, frame_width))
                frame_bits = extract_frame_bits_gpu(frame, frame_width, frame_height, block_size)
                bits += ''.join(map(str, frame_bits))
                progress.update(1)

    finally:
        ffmpeg_process.stdout.close()
        ffmpeg_process.wait()

    # Fehlerkorrekturbits entfernen und Bytes rekonstruieren
    byte_data = []
    byte_length = 8 + config["error_correction_bits"]
    for i in range(0, len(bits), byte_length):
        chunk = bits[i:i + byte_length]
        if len(chunk) < byte_length:
            break
        byte_data.append(int(chunk[:8], 2))

    # JSON-Metadaten extrahieren
    metadata_json = b""
    while byte_data and byte_data[0] != ord('\n'):
        metadata_json += bytes([byte_data.pop(0)])
    byte_data.pop(0)  # Entferne das Trennzeichen

    metadata = json.loads(metadata_json.decode('utf-8'))

    # ZIP-Datei erstellen
    zip_file = output_file + ".zip"
    with open(zip_file, "wb") as f:
        f.write(bytearray(byte_data))

    output_folder = os.path.dirname(output_file) or "./"
    extracted_files = decompress_file(zip_file, output_folder)

    try:
        if len(extracted_files) == 1:
            reconstructed_file = os.path.join(output_folder, extracted_files[0])
        elif os.path.exists(output_file):
            reconstructed_file = output_file
        else:
            raise FileNotFoundError(f"Keine Datei gefunden in: {output_folder}")

        # Metadaten anwenden
        set_file_metadata(reconstructed_file, metadata)
        print(f"Datei erfolgreich rekonstruiert: {reconstructed_file}")
    except Exception as e:
        print(f"Fehler beim Entpacken: {e}")
    finally:
        os.remove(zip_file)

# Hauptmenü
if __name__ == "__main__":
    print("Wähle eine Option:")
    print("1: Datei in ein Video konvertieren")
    print("2: Video in eine Datei rekonstruieren")

    choice = input("Gib 1 oder 2 ein: ").strip()

    if choice == "1":
        file_to_bw_video()
    elif choice == "2":
        video_to_file()
    else:
        print("Ungültige Auswahl. Programm wird beendet.")