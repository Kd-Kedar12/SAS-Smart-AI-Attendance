import numpy as np
import io
import librosa
import soundfile as sf
import streamlit as st

try:
    from resemblyzer import VoiceEncoder
    RESEMBLYZER_AVAILABLE = True
except Exception:
    RESEMBLYZER_AVAILABLE = False


if RESEMBLYZER_AVAILABLE:
    @st.cache_resource
    def load_voice_encoder():
        return VoiceEncoder()


    def _read_audio_bytes(audio_bytes, target_sr=16000):
        data, sr = sf.read(io.BytesIO(audio_bytes))
        if data is None:
            raise ValueError("No audio data found in bytes")
        # convert to mono
        if getattr(data, 'ndim', 1) > 1:
            data = np.mean(data, axis=1)
        # resample if needed
        if sr != target_sr:
            data = librosa.resample(data.astype('float32'), orig_sr=sr, target_sr=target_sr)
        return data.astype('float32')


    def get_voice_embedding(audio_bytes):
        try:
            if not audio_bytes:
                return None

            encoder = load_voice_encoder()
            audio = _read_audio_bytes(audio_bytes, target_sr=16000)
            embedding = encoder.embed_utterance(audio)
            return embedding.tolist()
        except Exception as e:
            st.error(f"Voice recognition failed: {e}")
            return None
else:
    def load_voice_encoder():
        return None

    def _read_audio_bytes(audio_bytes, target_sr=16000):
        raise RuntimeError('Resemblyzer is not installed')

    def get_voice_embedding(audio_bytes):
        st.error('Voice recognition engine not available (resemblyzer missing).')
        return None


def identify_speaker(new_embedding, candidate_dict, threshold=0.65):
    if new_embedding is None or not candidate_dict:
        return None, 0.0

    a = np.asarray(new_embedding, dtype=float)
    # normalize
    a_norm = a / (np.linalg.norm(a) + 1e-8)

    best_sid = None
    best_score = -1.0

    for sid, stored_embedding in candidate_dict.items():
        if not stored_embedding:
            continue
        b = np.asarray(stored_embedding, dtype=float)
        b_norm = b / (np.linalg.norm(b) + 1e-8)
        similarity = float(np.dot(a_norm, b_norm))
        if similarity > best_score:
            best_score = similarity
            best_sid = sid

    if best_score >= threshold:
        return best_sid, best_score

    return None, best_score



def process_bulk_audio(audio_bytes, candidate_dict, threshold=0.65):
    try:
        if not audio_bytes:
            return {}

        encoder = load_voice_encoder()

        audio = _read_audio_bytes(audio_bytes, target_sr=16000)
        segments = librosa.effects.split(audio, top_db=30)

        identified_results = {}

        sr = 16000
        for start, end in segments:

            if (end - start) < sr * 0.5:  # Skip segments shorter than 0.5 seconds
                continue

            segment_audio = audio[start:end]
            embedding = encoder.embed_utterance(segment_audio)

            sid, score = identify_speaker(embedding, candidate_dict, threshold)

            if sid:
                if sid not in identified_results or score > identified_results[sid]:
                    identified_results[sid] = score

        return identified_results
    except Exception as e:
        st.error(f'Bulk process error: {e}')
        return {}