import streamlit as st
from openai import OpenAI
import chromadb

client = OpenAI(api_key="key")

chroma_client = chromadb.PersistentClient(path="./apple_chroma_db")
collection = chroma_client.get_collection("apple_report")

# def ask(question, collection, client):
#     question_embedding = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=[question]
#     ).data[0].embedding
    
#     results = collection.query(
#         query_embeddings=[question_embedding],
#         n_results=3
#     )
    
#     context = "\n\n".join(results["documents"][0])
    
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a financial analyst. Answer questions using only the context provided. If the answer is not in the context, say so."
#             },
#             {
#                 "role": "user",
#                 "content": f"Context:\n{context}\n\nQuestion: {question}"
#             }
#         ]
#     )
    
#     return response.choices[0].message.content

def ask(question, collection, client):
    question_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=[question]
    ).data[0].embedding
    
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    
    context = "\n\n".join(results["documents"][0])
    pages = [r["page"] for r in results["metadatas"][0]]
    # print(context)
    # print(results['metadatas'])
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a financial analyst. Answer questions using only the context provided. If the answer is not in the context, say so."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )
    
    answer = response.choices[0].message.content
    citation = f"📄 Sources: Page {', '.join(str(p) for p in sorted(set(pages)))}"
    
    return answer, citation

# replace your current UI section with this
st.title("🍎 Apple Annual Report Q&A")
st.write("Ask any question about Apple's 2023 Annual Report")

# keep track of previous questions in the session
if "history" not in st.session_state:
    st.session_state.history = []

question = st.text_input("Your question:")

# if question:
#     with st.spinner("Searching report..."):
#         answer = ask(question, collection, client)
    
#     st.session_state.history.append({"q": question, "a": answer})

if question:
    with st.spinner("Searching report..."):
        answer, citation = ask(question, collection, client)
    
    st.markdown(f"**Answer:** {answer}")
    st.caption(citation)
    st.session_state.history.append({"q": question, "a": answer})
# show current answer
if st.session_state.history:
    latest = st.session_state.history[-1]
    st.markdown(f"**Answer:** {latest['a']}")
    
    # show previous questions
    if len(st.session_state.history) > 1:
        st.markdown("---")
        st.markdown("**Previous questions:**")
        for item in st.session_state.history[:-1]:
            st.markdown(f"**Q:** {item['q']}")
            st.markdown(f"**A:** {item['a']}")
            st.markdown("---")

# # UI starts here
# st.title("Apple Annual Report Q&A")
# st.write("Ask any question about Apple's 2023 Annual Report")

# question = st.text_input("Your question:")

# if question:
#     with st.spinner("Searching report..."):
#         answer = ask(question, collection, client)
#     st.write(answer)