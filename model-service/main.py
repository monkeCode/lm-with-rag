import grpc
import os
from grpc_files import lm_pb2, lm_pb2_grpc
import model
from concurrent import futures

PORT = os.getenv("grpc_port", 50001)

def messages_to_json(messages:list[lm_pb2.QueryMessage]) -> list[dict[str, str]]:
    return [{"role": m.author, "content":m.text} for m in messages]


class LmServiceServicer(lm_pb2_grpc.LanguageModelServicer):
    
    def Chat(self, request:lm_pb2.QuestionRequest, context):
        messages = messages_to_json(request.messages)
        for chunk in  model.generate_text(messages):
            yield lm_pb2.QuestionResponse(message=chunk)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lm_pb2_grpc.add_LanguageModelServicer_to_server(LmServiceServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    print(f"server starts at port: {PORT}")
    serve()