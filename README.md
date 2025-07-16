# Meta Transaction Test

이 프로젝트는 EIP-712 서명을 사용한 NFT 메타 트랜잭션 구현 테스트입니다.

## 환경 설정

1. Python 가상환경 생성 및 활성화
```bash
python3 -m venv venv
source venv/bin/activate
```

2. 필요한 패키지 설치
```bash
pip install web3 eth-account
```

## 주요 기능

### 1. NFT 메타 트랜잭션 전송
- EIP-712 서명을 사용하여 NFT 전송을 위한 메타 트랜잭션 구현
- 가스비를 릴레이어가 대신 지불하는 구조

### 2. 구현된 기능
- Web3 연결 및 컨트랙트 인스턴스 생성
- EIP-712 서명 생성
- 메타 트랜잭션 전송
- NFT 소유권 변경 확인

## 주요 수정사항

1. Web3 관련 수정
   - `LocalAccount` 객체의 private key 접근 방식 수정 (`private_key` → `key`)
   - 컨트랙트 주소를 체크섬 주소로 변환
   - Raw 트랜잭션 속성 이름 수정 (`rawTransaction` → `raw_transaction`)

2. 트랜잭션 영수증 접근 방식 수정
   - 속성 접근을 딕셔너리 방식으로 변경 (예: `tx_receipt.blockNumber` → `tx_receipt['blockNumber']`)

## 사용 방법

1. 환경 변수 설정
   - `USER_A_PRIVATE_KEY`: NFT 소유자의 개인키
   - `RELAYER_PRIVATE_KEY`: 릴레이어의 개인키
   - `CONTRACT_ADDRESS`: NFT 컨트랙트 주소
   - `TOKEN_ID`: 전송할 NFT의 토큰 ID
   - `TO_ADDRESS`: NFT를 받을 주소

2. 스크립트 실행
```bash
python meta-tx-test.py
```

## 주의사항

1. 실행 전 체크리스트:
   - 가상환경이 활성화되어 있는지 확인
   - Web3 연결 상태 확인
   - NFT 소유권 확인
   - 체인 ID 확인

2. 보안 주의사항:
   - 프라이빗 키는 안전하게 관리
   - 실제 환경에서는 환경변수나 설정 파일을 통해 관리 권장 