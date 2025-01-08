import grpc
from grpc_files import rag_pb2, rag_pb2_grpc
from concurrent import futures
import database_interface
import pandas_db
import os
from model_inference import LSTMModel, Attention
import model_inference
import metrics


PORT = os.getenv("grpc_port", 50001)

db: database_interface.DataBase = pandas_db.PandasDatabase("db.pickle")

class RagServiceServicer(rag_pb2_grpc.RagServiceServicer):
    def Vectorize(self, request, context):
        # TODO: make database vectorization
        result = len(request.documents)
        return rag_pb2.VectorizeResponse(result=result)

    def GetAnswer(self, request, context):
        
        embed = model_inference.embed(request.document)
        mins =  db.find_mins(embed, metrics.cosine_metric, 3)
        answers = []
        for min in mins:
            answers.append(rag_pb2.SimilarDocument(document=min[0], similarity=min[1]))
        return rag_pb2.GetAnswerResponse(answers=answers)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    rag_pb2_grpc.add_RagServiceServicer_to_server(RagServiceServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    print(f"server starts at port: {PORT} and device: {model_inference.DEVICE}")
    serve()