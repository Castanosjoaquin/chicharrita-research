import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import decode
from faster_whisper import WhisperModel
out_dir = sys.argv[1]; files = sys.argv[2:]
m = WhisperModel(os.environ.get("WMODEL","large-v3"), device="cpu", compute_type="int8", cpu_threads=8)
prompt = ("Investigathon, chicharrita del maíz, Dalbulus maidis, ARNi, ARN de doble cadena, dsRNA, siRNA, "
          "si-Fi21, dsRNA-Engineer, BLAST, off-target, transcriptoma, genoma, quimera, EPILAB, Spiroplasma, "
          "virus del rayado fino, energía libre, estructura secundaria, nucleótidos, ranking, benchmarking.")
for f in files:
    t = time.time(); audio = decode(f)
    segs, info = m.transcribe(audio, language="es", vad_filter=True, beam_size=1, condition_on_previous_text=False, initial_prompt=prompt)
    name = os.path.splitext(os.path.basename(f))[0]
    with open(os.path.join(out_dir, name + ".txt"), "w") as fh:
        fh.write(f"# {os.path.basename(f)} duracion={len(audio)/16000:.1f}s\n")
        for s in segs:
            mm, ss = divmod(int(s.start), 60)
            fh.write(f"[{mm:02d}:{ss:02d}] {s.text.strip()}\n"); fh.flush()
    print(name, f"{len(audio)/16000:.0f}s audio en {time.time()-t:.0f}s", flush=True)
print("LISTO", flush=True)
