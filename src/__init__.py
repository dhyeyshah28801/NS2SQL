import sounddevice as sd
import numpy as np
import librosa
import torch
from scipy.io.wavfile import write
from models.wave2vec import model, processor
from data.make_dataset import fetchDatabaseSchema
from models.rectifier import rectify_statement
from models.schema_retrieval import get_schema_from_query
from models.text_to_sql import nl_to_sql

# Recording configuration
samplerate = 16000  # Sampling rate for audio
duration = 10  # Duration of recording in seconds
audio_path = "recording.wav"

# Function to record audio
def record_audio():
    print("Recording... Please speak.")
    audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()  # Wait until the recording is finished
    print("Recording finished.")
    return audio_data

# Save audio to a file
def save_audio(audio_data, path, rate):
    write(path, rate, (audio_data * 32767).astype(np.int16))  # Convert to 16-bit PCM format

# Process audio through Wave2Vec model
def process_audio(audio_path):
    audio_data, sampling_rate = librosa.load(audio_path, sr=samplerate)

    # Preprocess audio data
    input_values = processor(audio_data, sampling_rate=samplerate, return_tensors="pt").input_values

    # Perform model prediction
    with torch.no_grad():
        logits = model(input_values).logits

    # Decode prediction results
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.decode(predicted_ids[0])
    return transcription

# Main flow
audio_data = record_audio()
save_audio(audio_data, audio_path, samplerate)
transcription = process_audio(audio_path)
dbSchema = fetchDatabaseSchema('./data/db_schema.json')
rectified_statement = rectify_statement(dbSchema, transcription)
schema = get_schema_from_query(rectified_statement)
sql_query = nl_to_sql(rectified_statement, schema=schema)

# Output results
print(f"Predicted SQL Query: {sql_query}")
