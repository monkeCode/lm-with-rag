import grpc
from grpc_files import rag_pb2, rag_pb2_grpc

PORT = 50001


def run():
    with grpc.insecure_channel(f'localhost:{PORT}') as channel:
        stub = rag_pb2_grpc.RagServiceStub(channel)

        # Пример запроса Vectorize
        vectorize_request = rag_pb2.VectorizeRequest(documents=["doc1", "doc2", "doc3"])
        vectorize_response = stub.Vectorize(vectorize_request)
        print(f"Vectorize Response: {vectorize_response.result}")

        # Пример запроса GetAnswer
        get_answer_request = rag_pb2.GetAnswerRequest(document="calculate $\sin(5x)$")
        get_answer_response = stub.GetAnswer(get_answer_request)
        for answer in get_answer_response.answers:
            print(f"Document: {answer.document}\n Similarity: {answer.similarity}")
            print("="* 10)

if __name__ == '__main__':
    run()
