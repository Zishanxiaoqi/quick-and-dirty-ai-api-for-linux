import sys
import argparse
import openai
import select

def get_reponse(question, file_in = ""  , role_system = "你是一个有用的助手" ,max_tokens = 1024 , model_flag = 0):
    client = openai.OpenAI(api_key="", base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat" if not model_flag else "deepseek-reasoner",
        messages=[
            {"role": "system", "content": role_system  },
            {"role": "user", "content": f"{file_in},问题:{question}"},
    ],
        max_tokens=max_tokens,
        temperature=0.7,
        stream=False
    )
    return response.choices[0].message.content if not model_flag else  response.choices[0].message.reasoning_content + "\n" +response.choices[0].message.content 
def main():
    parser = argparse.ArgumentParser(description="OpenAI API Chatbot")
    parser.add_argument("-q","--question", required= True,help="Question to ask the chatbot")
    parser.add_argument("file", nargs = "?" ,type=argparse.FileType("r") ,  default=sys.stdin, help="Input file to be analyzed")
    parser.add_argument("-r", "--role", required = False,default="你是一个有用的助手", help="Role of the chatbot")
    parser.add_argument("-l","--limit", required = False,default=1024, type=int, help="Max tokens for the response")
    parser.add_argument("-m","--model",action= "store_true", help="Use the model for the response")

    args = parser.parse_args()

    file_in = args.file.read().strip() if  select.select([sys.stdin], [], [], 0)[0] else ""
    
    limit = args.limit
    question = args.question
    role_system = args.role
    response = get_reponse(question, "" if not file_in else f"提供的数据为{file_in}", role_system, limit, args.model)
    print(response)

    

if __name__ == "__main__":
    main()
