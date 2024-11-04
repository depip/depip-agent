# Depip agent

## Overview architecture  
```mermaid
---
title: Sequence diagram create knowledge
---
sequenceDiagram 
    Admin->>+Agent: Put knowledge (pdf, web crawler)
    Admin->>+Agent: create vector store
    Agent->>+Embedding Model: create vector store
    Embedding Model-->>-Agent: vector store
    Agent->>-Storage: save vector store
```

```mermaid
---
title: Sequence diagram invoke agent
---
sequenceDiagram 
    User->>+Agent: Invoke agent
    Agent->>+Embedding Model: get knowledge
    Embedding Model->>Embedding Model: get knowledge from storage
    Embedding Model-->>-Agent: knowledge
    Agent->>Agent: create answer
    Agent-->>-User: answer
```


```mermaid
---
title: Flow diagram depip agent
---
flowchart LR

subgraph "Depip agent"

    subgraph "Agent"
        direction TB
        memory[memory]
        agent-executor[agent executor]
        tools[tools]
        llm-model[LLM model]
        agent-executor <--> memory
        agent-executor <--> tools
        agent-executor --> llm-model
    end

    subgraph "Embedding Model" 
        direction TB
        web-crawled[web crawled]
        pdf[files pdf]
        embedding-model[embedding model]
        vector-store[vector store]
        s3 --> embedding-model --> vector-store
        web-crawled --> embedding-model
        pdf --> embedding-model
    end  
    tools --> vector-store
end
```  
```mermaid
---
title: Class diagram depip agent
---
classDiagram
    direction TD
   
    BaseModelLangchain --|> EmbeddingModel
    EmbeddingsLangchain --|> EmbeddingModel
    class EmbeddingModel{
        embedding_model
        createEmbeddingPDF()
        loadVectorStore()
    }
    BaseChatModelLangchain --|> LLMModel
    class LLMModel{
        llm_model
    }
    class BaseModelLangchain{
    }
    class EmbeddingsLangchain{
    }
    
    class Agent{
        invoke(query)
    }
    EmbeddingModel -- Agent
    LLMModel -- Agent


```

Currently features:
- Chat with model with preload vector store (has knowledge about Story Protocol)

## How to run
### 1. Prequisite
- Miniconda
- Python3
### 2. Install
```sh
conda env create --file environment.yml          
conda activate depip-agent
pip install -r requirements.txt  
```
### 3. Start app
```sh
fastapi run app/main.py
```