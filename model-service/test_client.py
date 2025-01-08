import grpc
from grpc_files import lm_pb2, lm_pb2_grpc

PORT = 50001

def run():
    with grpc.insecure_channel(f'localhost:{PORT}') as channel:
        stub = lm_pb2_grpc.LanguageModelStub(channel)

        # Пример запроса Chat
        question_request = lm_pb2.QuestionRequest(messages=[lm_pb2.QueryMessage(author = "system", text="you are an helpful assistant"),  
                                                            lm_pb2.QueryMessage(author = "user", text="hello")])
        responses = stub.Chat(question_request)

        for response in responses:
            print(f"Received message: {response.message}")

if __name__ == '__main__':
    run()
