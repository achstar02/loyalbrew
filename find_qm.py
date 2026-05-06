import sys
sys.stdout.reconfigure(encoding='utf-8')

f = 'C:/Users/Administrator/CodeBuddy/20260416214625/index.html'
with open(f, 'rb') as fh:
    raw = fh.read()

# Find LoyalBrew in title
target = b'LoyalBrew'
idx = raw.find(target)
print(f'LoyalBrew at byte offset: {idx}')
if idx >= 0:
    ctx = raw[idx:idx+50]
    print(f'Raw bytes: {ctx}')
    try:
        print(f'Decoded: {ctx.decode("utf-8")}')
    except:
        print(f'Decoded (replace): {ctx.decode("utf-8", errors="replace")}')

# Also search for question mark bytes 0x3F
q_positions = [i for i, b in enumerate(raw) if b == 0x3F]
print(f'\nTotal "?" bytes (0x3F): {len(q_positions)}')

# Find clusters of consecutive ? 
clusters = []
if q_positions:
    start = q_positions[0]
    count = 1
    for p in q_positions[1:]:
        if p == start + count:
            count += 1
        else:
            if count >= 2:
                clusters.append((start, count))
            start = p
            count = 1
    if count >= 2:
        clusters.append((start, count))

print(f'\nClusters of 2+ consecutive "?": {len(clusters)}')
for start, count in clusters[:15]:
    ctx = raw[max(0,start-5):start+count+10]
    text = ctx.decode('utf-8', errors='replace')
    print(f'  offset {start} ({count}?): ...{text}...')
