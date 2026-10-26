import sys, numpy as np, av
def decode(path, rate=16000):
    with av.open(path, mode="r") as c:
        st = c.streams.audio[0]
        st.thread_type = "AUTO"
        rs = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=rate)
        chunks = []
        for frame in c.decode(st):
            for f in rs.resample(frame):
                chunks.append(f.to_ndarray().reshape(-1))
        for f in rs.resample(None):
            chunks.append(f.to_ndarray().reshape(-1))
    a = np.concatenate(chunks).astype(np.float32) / 32768.0
    return a
if __name__ == "__main__":
    a = decode(sys.argv[1]); print(len(a)/16000.0, "s")
