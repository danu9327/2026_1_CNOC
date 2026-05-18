import gzip
import os
import re
import json

# 1. 설정
base_path = r'C:\Users\user\Desktop\ㅎ\국방\2026\2026_1_CNOC\data\raw_data\Splunk_BOTSv3\botsv3_data_set\var'
output_file = 'C:/Users/user/Desktop/ㅎ/국방/2026/2026_1_CNOC/data/preprocess_data/bots_v3_network_logs.json'

# 폴더 생성
output_dir = os.path.dirname(output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 2. 네트워크 로그를 상징하는 핵심 키(Key)들
network_keys = {'src_ip', 'dest_ip', 'src_port', 'dest_port'}

extracted_data = []
file_count = 0

print("네트워크 데이터 추출 중... (네트워크 필드 감지 방식)")

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file == 'journal.gz':
            file_path = os.path.join(root, file)
            file_count += 1
            
            with gzip.open(file_path, 'rb') as f:
                for line in f:
                    try:
                        line_str = line.decode('utf-8', errors='ignore')
                        # 한 줄에 여러 JSON이 있을 수 있으므로 findall 사용
                        matches = re.findall(r'(\{.*?\})', line_str)
                        
                        for match in matches:
                            try:
                                event = json.loads(match)
                                
                                # 로직 수정: 특정 키들이 포함되어 있는지 확인 (교집합 확인)
                                # src_ip와 dest_ip가 둘 다 있으면 네트워크 로그로 판단
                                if network_keys.issubset(event.keys()):
                                    extracted_data.append(event)
                                    
                                    # 진행 상황 출력 (1000개 단위)
                                    if len(extracted_data) % 1000 == 0:
                                        print(f"현재 {len(extracted_data)}개 추출 완료...")
                                        
                            except json.JSONDecodeError:
                                continue
                    except Exception:
                        continue

# 3. 저장
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump(extracted_data, out, ensure_ascii=False, indent=4)

print(f"\n[추출 종료]")
print(f"- 조사한 journal.gz 파일 수: {file_count}")
print(f"- 최종 추출된 네트워크 로그 수: {len(extracted_data)}")