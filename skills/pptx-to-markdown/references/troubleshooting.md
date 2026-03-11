# Troubleshooting

## 텍스트 추출 문제

### 텍스트가 전혀 추출되지 않음
- 슬라이드가 이미지만으로 구성되어 있을 수 있음 (스캔된 자료).
  → `ocr-document-processor` 스킬로 OCR 처리 후 변환.
- `python-pptx`가 설치되지 않았을 수 있음. `pip install python-pptx` 수동 실행.

### 한글/CJK 텍스트 깨짐
- python-pptx는 유니코드를 직접 읽으므로 대부분 문제 없음.
- 여전히 깨지면 파일 자체가 손상된 경우일 수 있음.
  → LibreOffice로 열어서 다시 저장 후 시도.

### 텍스트 순서가 뒤섞임
- 복잡한 레이아웃(겹쳐진 텍스트 박스, 멀티 컬럼)일 수 있음.
- Shape의 위치(top, left) 기준으로 정렬되지만, 완벽하지 않을 수 있음.
- Claude 정제 단계에서 "내용 순서를 논리적으로 재정렬해줘"라고 요청.

## 구조 감지 문제

### 제목이 감지되지 않음
- 슬라이드에 Title placeholder 대신 일반 텍스트 박스를 제목으로 사용한 경우.
- Claude 정제 시 "각 슬라이드의 첫 번째 굵은 텍스트를 제목으로 변환해줘"라고 요청.

### 리스트 중첩이 깨짐
- python-pptx의 `para.level`이 0으로 동일하게 나오는 경우.
  → 슬라이드 원본에서 indent level이 설정되지 않은 것.
- Claude 정제 시 "들여쓰기 구조를 콘텐츠 기반으로 추론해줘"라고 요청.

### 테이블이 변환되지 않음
- 테이블처럼 보이지만 실제로는 정렬된 텍스트 박스일 수 있음.
  → Claude에게 "이 부분을 테이블로 변환해줘"라고 요청.

## 이미지/미디어 문제

### 이미지 내용을 추출하고 싶음
- python-pptx는 이미지 텍스트를 읽을 수 없음.
- 이미지가 많은 슬라이드는 `ocr-document-processor` 스킬을 병행 사용.

### 차트 데이터를 추출하고 싶음
- python-pptx로 차트 데이터(Excel 내장 데이터)에 접근할 수 있으나 복잡함.
- 현재 스크립트는 `[차트]` 플레이스홀더로 표시. 차트 데이터가 필요하면 Claude에게 추가 처리를 요청.

## 파일 열기 실패

### "Package not found" 에러
- 파일이 `.pptx`가 아닌 `.ppt` (구형 형식)일 수 있음.
  → LibreOffice로 열어서 `.pptx`로 내보내기 후 시도:
  ```bash
  libreoffice --headless --convert-to pptx lecture.ppt
  ```

### 암호화된 PPTX
- python-pptx는 암호화된 PPTX를 열 수 없음.
  → LibreOffice로 열어서 암호 제거 후 저장, 또는:
  ```bash
  # msoffcrypto-tool 사용
  pip install msoffcrypto-tool
  python3 -c "
  import msoffcrypto, io
  with open('encrypted.pptx', 'rb') as f:
      office = msoffcrypto.OfficeFile(f)
      office.load_key(password='PASSWORD')
      with open('decrypted.pptx', 'wb') as out:
          office.decrypt(out)
  "
  ```

## 성능

### 슬라이드 수가 많아 느림
- `--slides` 옵션으로 범위를 나눠서 처리:
  ```bash
  python3 convert_pptx.py -i big.pptx --slides 1-50
  python3 convert_pptx.py -i big.pptx --slides 51-100
  ```
