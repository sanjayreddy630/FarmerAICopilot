 🌱 Farmer AI Copilot

Farmer AI Copilot is an AI-powered agricultural assistant designed to help farmers identify crop and pest problems, ask agriculture-related questions, and receive source-grounded recommendations.

The application combines **AI image analysis**, **Retrieval-Augmented Generation (RAG)**, multilingual support, and a simple farmer-friendly interface.

---

## 🚀 Features

### 🌿 Crop & Pest Image Analysis

- Upload a crop or pest image.
- Capture an image using the device camera.
- AI analyzes the image.
- Provides information about the possible crop disease or pest.
- Gives recommendations based on the analysis.

### 🤖 AI Agricultural Assistant

Farmers can ask questions such as:

- What disease is affecting my crop?
- How can I control pests?
- What fertilizer should I use?
- How often should I water my crop?
- What are the symptoms of a particular disease?

### 📚 RAG-Based Answers

Farmer AI Copilot uses **Retrieval-Augmented Generation (RAG)** to provide answers using relevant agricultural information.

The RAG pipeline includes:

1. Document ingestion
2. Document chunking
3. Embedding generation
4. Vector retrieval
5. Re-ranking
6. Context building
7. AI-generated response

This helps the system provide answers grounded in the available agricultural knowledge and sources.

### 🌍 Multilingual Support

The application supports:

- English
- Hindi
- Telugu

The interface and responses can be provided according to the selected language.

### 📷 Camera Support

Farmers can:

1. Open the camera.
2. Capture a crop/pest image.
3. Preview the image.
4. Send the image to the backend.
5. Receive AI analysis.

Camera access requires browser permission.

---
## 🛠️ Technologies Used

### Frontend

#### ⚛️ React + Vite
- Main web application interface
- Responsive UI
- Background and visual interface
- Chat interface
- Image upload
- Camera capture
- Language selection
- English / Hindi / Telugu support

#### 🐍 Streamlit
- AI/RAG interface
- Text input boxes
- Agricultural query interface
- Source-grounded response display
- RAG testing and interaction
- AI model interaction

### Backend
- Python
- Flask
- REST APIs

### AI & RAG
- Retrieval-Augmented Generation (RAG)
- Document ingestion
- Chunking
- Embeddings
- Vector retrieval
- Re-ranking
- Context building
- LLM-based response generation

### Image Analysis
- AI image model
- Crop/pest analysis
- Disease identification
- Classification
- Prediction
- Agricultural recommendations

### Multilingual Support
- English
- Hindi
- Telugu

### Deployment & Version Control
- GitHub
- Render

# 🏗️ Project Architecture

```text
                         ┌──────────────────────┐
                         │      Farmer/User     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │      Streamlit Frontend     │
                    │                             │
                    │  • Chat Interface           │
                    │  • Text Input               │
                    │  • English / Hindi / Telugu│
                    │  • Source Display           │
                    │  • AI Interaction           │
                    │  • Image Upload             │
                    │  • Camera Input             │
                    └──────────────┬──────────────┘
                                   │
                              API Requests
                                   │
                                   ▼
                    ┌─────────────────────────────┐
                    │       Flask Backend         │
                    │                             │
                    │  /api/ask                   │
                    │  /api/upload                │
                    │  /api/analyze-image         │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌─────────────────┐           ┌─────────────────┐
          │    RAG System   │           │  Image Model    │
          │                 │           │                 │
          │ Document        │           │ Crop/Disease    │
          │ Chunking        │           │ Analysis        │
          │ Retrieval       │           │                 │
          │ Re-ranking      │           │                 │
          │ Context         │           │                 │
          │ Building        │           │                 │
          └────────┬────────┘           └────────┬────────┘
                   │                             │
                   └──────────────┬──────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   AI Response    │
                         │                  │
                         │ Source-Grounded  │
                         │ Agricultural     │
                         │ Intelligence     │
                         └──────────────────┘

                         👨‍🌾 Farmer
                         
     
