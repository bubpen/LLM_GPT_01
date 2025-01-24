import openai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API Key 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 프롬프트 명령
prompt = "You are a very scary computer teacher."

# 초기 대화 설정
messages = [{"role": "sytem", "content": prompt}]

# exit가 입력되기 전까지 계속 대화할 거예요
while True:
    # 사용자 입력받기
    user_input = input("User: ")
    
    # "exit" 입력 시 대화 종료
    if user_input.lower() == "exit":
        print("대화를 종료합니다.")
        break
    
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "You are a best programmer"}, # 프롬프트 명령
            {"role": "user", "content" : user_input} # 사용자 입력
        ]
    )
    
    print(response['choices'][0]['message']['content'])
