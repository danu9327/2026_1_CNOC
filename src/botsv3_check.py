import json
import random
from collections import Counter

# 1. 데이터 로드
with open('C:/Users/user/Desktop/ㅎ/국방/2026/2026_1_CNOC/data/preprocess_data/bots_v3_network_logs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✅ 총 이벤트 개수: {len(data):,}개")

# 2. 통계 분석 (네트워크 레벨 증명용)
dest_ports = Counter()
protocols = Counter()
sourcetypes = Counter()

for event in data:
    # 목적지 포트 통계
    port = event.get('dest_port') or event.get('destination_port')
    if port: dest_ports[port] += 1
    
    # 프로토콜 통계
    proto = event.get('transport') or event.get('protocol')
    if proto: protocols[proto] += 1

# 3. 결과 출력: 상위 10개 포트 (네트워크 서비스 확인)
print("\n📊 [네트워크 서비스 분포 - Top 10 Ports]")
print("포트번호 | 빈도수 | 주요 서비스")
print("-" * 35)
port_map = {53: "DNS", 80: "HTTP", 443: "HTTPS", 22: "SSH", 445: "SMB"}
for port, count in dest_ports.most_common(10):
    service = port_map.get(int(port) if str(port).isdigit() else port, "Other")
    print(f"{str(port):<8} | {count:<7} | {service}")

# 4. 무작위 샘플링 (눈으로 확인)
print("\n🔍 [무작위 데이터 샘플 (3개)]")
samples = random.sample(data, 3)
for i, sample in enumerate(samples):
    print(f"\n--- Sample {i+1} ---")
    print(json.dumps(sample, indent=4, ensure_ascii=False))