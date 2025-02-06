This is my pet project inferencing language model with RAG system.
# State
- [x] backend - almost done
- [x] llm service - done
- [x] rag service - done except db
- [ ] frontend - in progress 
# Deployment diagram
![image](https://github.com/user-attachments/assets/17f9c221-8f62-4381-a05a-b3397c540aae)

document-db, phi3 and gRPC services can be replaced with others as long as they fit into the interfaces.

# Rag Model
  Model for encoding and searchnig similar documents was developed by me, and you can view the pipeline of its development at Kaggle [Model notebook](https://www.kaggle.com/code/jorjo2009/math-problems-rag/notebook).
  There are two models: LSTM with attention mechanism and transformer with relative possition encoding in multihead attention. As loss function was used constastive loss function 
  $L^{contrast} = \sum_i || q_i - a_i ||^2_2 +  \sum_i \sum_{j, i \neq j}  (bound - || q_i-a_j||^2_2)_+$

# Deployment
> [!IMPORTANT]
> Before deployment you should add some files
> - /model-service/settings.conf with your hugging face token like hf_xxxxxxxxxxxxxxxxxx
> - /kubernetes/secrets.yaml: 
> ```yaml
> apiVersion: v1
> kind: Secret
> metadata:
>  name: mysql-secret
> type: Opaque
> stringData:
>  MYSQL_ROOT_PASSWORD: "somepass"
>  MYSQL_USER: "someuser"
>  MYSQL_PASSWORD: "somepass2"
>  MYSQL_DATABASE: "somedb"
> ```
> - /rag-service/db.pickle if you want to use pandas as local database for your documents
