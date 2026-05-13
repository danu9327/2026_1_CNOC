import gzip
import os
import re
import json

# 1. 설정: BOTS v3 데이터 경로 및 저장 파일명
base_path = r'C:\Users\user\Downloads\botsv3_data_set\botsv3_data_set\var\lib\splunk\botsv3\db'
output_file = 'bots_v3_network_logs.json'

# 2. 필터링할 네트워크 관련 sourcetype (화이트리스트)
network_sourcetypes = [
    'pan:traffic', 'pan:threat', 'fortigate_utm', 
    'stream:http', 'stream:dns', 'stream:tcp', 'stream:udp', 'stream:icmp',
    'aws:cloudwatch:vpcflow', 'cisco:asa'
]

# 3. JSON 추출을 위한 정규표현식 ( {로 시작해서 }로 끝나는 패턴 )
json_pattern = re.compile(r'(\{.*\})')

extracted_data = []

print("데이터 추출을 시작합니다. 잠시만 기다려 주세요...")

# 모든 db_ 디렉토리 순회
for root, dirs, files in os.walk(base_path):
    if 'rawdata' in root:
        for file in files:
            if file == 'journal.gz':
                file_path = os.path.join(root, file)
                
                with gzip.open(file_path, 'rb') as f:
                    for line in f:
                        try:
                            line_str = line.decode('utf-8', errors='ignore')
                            match = json_pattern.search(line_str)
                            
                            if match:
                                raw_json = match.group(1)
                                event = json.loads(raw_json)
                                
                                # sourcetype 필터링 (네트워크 관련 로그만)
                                # Splunk journal 내부 구조상 sourcetype 위치를 확인하여 필터링
                                # 보통 이벤트 내부에 포함되거나 메타데이터에 존재함
                                if any(st in line_str for st in network_sourcetypes):
                                    extracted_data.append(event)
                                    
                        except Exception:
                            continue

# 4. 최종 결과 저장 (JSON 포맷)
with open(output_file, 'w', encoding='utf-8') as out:
    json.dump(extracted_data, out, ensure_ascii=False, indent=4)

print(f"추출 완료! 총 {len(extracted_data)}개의 네트워크 로그가 {output_file}에 저장되었습니다.")