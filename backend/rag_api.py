import grpc
from grpc_files import rag_pb2, rag_pb2_grpc

class Rag:

    def __init__(self, address, port):
        self.address = address
        self.port = port

    async def get_answers(self, document:str)-> list[(str, float)]:
        with grpc.insecure_channel(f'{self.address}:{self.port}') as channel:

            stub = rag_pb2_grpc.RagServiceStub(channel)
            get_answer_request = rag_pb2.GetAnswerRequest(document=document)
            get_answer_response = stub.GetAnswer(get_answer_request)

        return [{"document": answer.document, "similarity":answer.similarity} for answer in get_answer_response.answers]