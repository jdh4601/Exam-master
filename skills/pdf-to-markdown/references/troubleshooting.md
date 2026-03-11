# Troubleshooting

## 복호화 실패

### "Wrong password" 에러
- 비밀번호가 정확한지 확인. 공백, 대소문자 주의.

### pypdf로 열 수 없는 암호화
일부 PDF는 pypdf가 지원하지 않는 암호화 사용. pikepdf로 대체:
```bash
pip install pikepdf
python3 -c "
import pikepdf
pdf = pikepdf.open('input.pdf', password='PASSWORD')
pdf.save('decrypted.pdf')
"
```
복호화된 파일을 `--input`으로 전달하면 됨.

## 텍스트 추출 문제

### 텍스트가 전혀 추출되지 않음
- PDF가 이미지 기반(스캔)일 수 있음. OCR이 필요 → `ocr-document-processor` 스킬 사용.
- `pdfplumber`가 설치되지 않았을 수 있음. `pip install pdfplumber` 수동 실행.

### 한글/CJK 텍스트 깨짐
- 폰트 임베딩 문제. pdfplumber는 대부분 처리 가능.
- 여전히 깨지면: `page.extract_text(layout=True)` 시도.

### 글자 순서가 뒤섞임
- 다단(multi-column) 레이아웃일 수 있음.
- 페이지 범위를 좁혀서 문제 페이지를 찾고, Claude에게 정제 요청.

## 구조 감지 문제

### 헤딩이 감지되지 않음
- 모든 텍스트가 같은 폰트 크기면 감지 불가.
- Claude 정제 단계에서 내용 기반으로 헤딩 구조를 추가.

### 테이블이 일반 텍스트로 추출됨
- 경계선 없는 테이블은 pdfplumber가 감지 못할 수 있음.
- Claude 정제 시 "테이블 구조를 복원해줘"라고 요청.

## 성능

### 대용량 PDF가 느림
- `--pages` 옵션으로 범위를 나눠서 처리:
  ```bash
  python3 convert_pdf.py -i big.pdf -p "1234" --pages 1-50
  python3 convert_pdf.py -i big.pdf -p "1234" --pages 51-100
  ```
