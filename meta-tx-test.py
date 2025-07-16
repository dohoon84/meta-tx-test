import json
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_typed_data

# ==============================================================================
# 1. 설정 변수 (사용자 환경에 맞게 채워주세요)
# ==============================================================================

# 아발란체 AEM RPC URL
RPC_URL = "http://43.201.35.39:9650/ext/bc/C/rpc"

# 4단계에서 배포한 컨트랙트 주소
CONTRACT_ADDRESS = "0x62a53Be547930d2b199Ef139F27A63c3Af2691C3"

# 2단계에서 준비한 비공개 키
USER_A_PRIVATE_KEY = "0xa77e1a4c444bb85a35db32e1bdcc71569be78b812a14712963d48f46aa49b661"           # NFT 소유자 (서명만 함)
RELAYER_PRIVATE_KEY = "0x5796368c3c6f8be68f803b659a00e7389c5300ec3e4e0a20d3e66d5c059983af"         # 가스비 지불자

# 5단계에서 민팅한 NFT 정보
TOKEN_ID = 2

# NFT를 받을 주소 (새로운 주소 또는 릴레이어 주소 등)
USER_B_ADDRESS = "0xFF6F9189507a845Ee545C629B9E93e0a67e69d68" # 전송받을 주소 입력

# 4단계에서 복사한 컨트랙트 ABI
CONTRACT_ABI = """
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "addAdmin",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "name_",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "symbol_",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "baseTokenURI_",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "initialAdmin",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "approved",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "operator",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "bool",
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "ApprovalForAll",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "burn",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			},
			{
				"internalType": "bytes",
				"name": "signature",
				"type": "bytes"
			}
		],
		"name": "executeMetaTransferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "mint",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "removeAdmin",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			},
			{
				"internalType": "bytes",
				"name": "data",
				"type": "bytes"
			}
		],
		"name": "safeTransferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "operator",
				"type": "address"
			},
			{
				"internalType": "bool",
				"name": "approved",
				"type": "bool"
			}
		],
		"name": "setApprovalForAll",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "getApproved",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "isAdmin",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "operator",
				"type": "address"
			}
		],
		"name": "isApprovedForAll",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "nonces",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "ownerOf",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes4",
				"name": "interfaceId",
				"type": "bytes4"
			}
		],
		"name": "supportsInterface",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "tokenId",
				"type": "uint256"
			}
		],
		"name": "tokenURI",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
"""

# ==============================================================================
# 2. Web3 연결 및 계정 설정
# ==============================================================================

w3 = Web3(Web3.HTTPProvider(RPC_URL))

# 계정 로드
user_a = Account.from_key(USER_A_PRIVATE_KEY)
relayer = Account.from_key(RELAYER_PRIVATE_KEY)

# 컨트랙트 인스턴스 생성
contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=json.loads(CONTRACT_ABI)
)

print(f"Web3 연결 상태: {w3.is_connected()}")
print(f"사용자 A 주소: {user_a.address}")
print(f"릴레이어 주소: {relayer.address}")
print(f"컨트랙트 이름: {contract.functions.name().call()}")
print(f"Chain ID: {w3.eth.chain_id}")
try:
    print(f"NFT 소유자: {contract.functions.ownerOf(TOKEN_ID).call()}")
except Exception as e:
    print(f"NFT 소유권 확인 실패: {str(e)}")
print("-" * 60)


# ==============================================================================
# 3. 메타 트랜잭션 서명 생성 (사용자 A)
# ==============================================================================

def generate_meta_tx_signature():
    print("1. 메타 트랜잭션 서명 생성을 시작합니다...")

    # a. 컨트랙트에서 사용자 A의 현재 nonce 조회 (블록체인 읽기, 가스비 없음)
    nonce = contract.functions.nonces(user_a.address).call()
    print(f"   - 사용자 A의 현재 Nonce: {nonce}")

    # b. EIP-712 타입 데이터 구조화 (컨트랙트와 완벽히 일치해야 함)
    typed_data = {
        "types": {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
                {"name": "chainId", "type": "uint256"},
                {"name": "verifyingContract", "type": "address"},
            ],
            "MetaTransferFrom": [
                {"name": "from", "type": "address"},
                {"name": "to", "type": "address"},
                {"name": "tokenId", "type": "uint256"},
                {"name": "nonce", "type": "uint256"},
            ],
        },
        "primaryType": "MetaTransferFrom",
        "domain": {
            "name": "test",    # 실제 컨트랙트 이름
            "version": "1",     # 컨트랙트 버전
            "chainId": w3.eth.chain_id,
            "verifyingContract": CONTRACT_ADDRESS,
        },
        "message": {
            "from": user_a.address,
            "to": USER_B_ADDRESS,
            "tokenId": TOKEN_ID,
            "nonce": nonce,
        },
    }

    # c. 사용자 A의 키로 데이터에 서명 (오프라인 작업, 가스비 없음)
    signable_message = encode_typed_data(full_message=typed_data)
    signed_message = Account.sign_message(signable_message, private_key=user_a.key)

    print("   - EIP-712 서명 생성 완료!")
    return signed_message.signature

# ==============================================================================
# 4. 트랜잭션 전송 (릴레이어)
# ==============================================================================

def send_meta_transaction(signature):
    print("2. 릴레이어가 트랜잭션을 전송합니다...")

    # a. 트랜잭션 실행 전 NFT 소유자 확인
    owner_before = contract.functions.ownerOf(TOKEN_ID).call()
    print(f"   - 전송 전 NFT 소유자: {owner_before}")
    assert owner_before == user_a.address

    # b. 릴레이어가 실행할 함수 호출 데이터 구성
    tx_data = contract.functions.executeMetaTransferFrom(
        user_a.address,     # from
        USER_B_ADDRESS,     # to
        TOKEN_ID,           # tokenId
        signature           # 사용자 A의 서명
    ).build_transaction({
        'from': relayer.address,
        'nonce': w3.eth.get_transaction_count(relayer.address),
        'gasPrice': w3.eth.gas_price,
    })

    # c. 가스비 추정 및 설정
    estimated_gas = w3.eth.estimate_gas(tx_data)
    tx_data['gas'] = estimated_gas
    print(f"   - 예상 가스비: {estimated_gas}")

    # d. 릴레이어의 키로 트랜잭션 서명
    signed_tx = w3.eth.account.sign_transaction(tx_data, relayer.key)
    print("   - 릴레이어가 트랜잭션에 서명했습니다.")

    # e. 서명된 Raw Transaction 전송
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    print(f"   - 트랜잭션 전송 완료! Tx Hash: {tx_hash.hex()}")

    # f. 트랜잭션 처리 대기
    print("   - 트랜잭션이 블록에 포함되기를 기다리는 중...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"   - 트랜잭션 처리 완료! 블록 번호: {tx_receipt['blockNumber']}")

    # g. 결과 확인
    owner_after = contract.functions.ownerOf(TOKEN_ID).call()
    print(f"3. 결과 확인:")
    print(f"   - 전송 후 NFT 소유자: {owner_after}")

    if owner_after == USER_B_ADDRESS:
        print("✅ 테스트 성공: NFT가 성공적으로 전송되었습니다!")
    else:
        print("❌ 테스트 실패: NFT 소유자가 변경되지 않았습니다.")


# ==============================================================================
# 5. 스크립트 실행
# ==============================================================================

if __name__ == "__main__":
    user_signature = generate_meta_tx_signature()
    send_meta_transaction(user_signature)
