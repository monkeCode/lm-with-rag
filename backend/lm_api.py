import grpc
from grpc_files import lm_pb2, lm_pb2_grpc
import entities

class Lm():

    def __init__(self, address, port):
        self.address = address
        self.port = port

    def generate_text(self, documents:list[entities.Message]):
        messages = [ lm_pb2.QueryMessage(author = message.author, text=message.text) for message in documents]
        with grpc.insecure_channel(f'{self.address}:{self.port}') as channel:
            stub = lm_pb2_grpc.LanguageModelStub(channel)
            
            
            question_request = lm_pb2.QuestionRequest(messages=messages)
            responses = stub.Chat(question_request)

            for response in responses:
                yield response.message