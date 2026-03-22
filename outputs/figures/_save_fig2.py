import base64, os

b64 = ""
for i in range(9):
    chunk_path = rf"C:\infovail-iq\outputs\figures\_chunk_{i:02d}.txt"
    with open(chunk_path, 'r') as f:
        b64 += f.read()

data = base64.b64decode(b64)
out_path = r"C:\infovail-iq\outputs\figures\figure2_7C_prevalence_v2.png"
with open(out_path, 'wb') as f:
    f.write(data)
print(f"Saved {len(data)} bytes to {out_path}")
