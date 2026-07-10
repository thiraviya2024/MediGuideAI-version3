from utils.llm import client

def ask_ai(vectorstore, question: str) -> str:
    """
    Enhanced AI Medical Report Assistant.
    Combines RAG retrieval with intelligent medical interpretation.
    """
    
    # Retrieve relevant context
    docs = vectorstore.similarity_search(question, k=4)
    context = "\n\n".join([doc.page_content for doc in docs])

    system_prompt = """
You are MediGuide AI, a compassionate and knowledgeable AI Medical Report Assistant.
Your goal is to help patients clearly understand their medical reports and what the findings mean in simple, everyday language.

Core Rules:
1. Always base your answer primarily on the uploaded medical report.
2. You may use general medical knowledge to explain terms, implications, risks, or lifestyle suggestions when they are directly related to findings in the report.
3. Never diagnose diseases, prescribe medicines, or give personalized medical treatment plans.
4. Never invent values or test results that are not in the report.
5. If something is not mentioned in the report, clearly say so.
6. Use simple, empathetic, and non-alarming language.
7. Always encourage consulting a qualified doctor for professional advice.
8. For dietary or lifestyle suggestions, keep them general and clearly state they are not personalized.

Tone: Professional yet warm, like a caring doctor explaining to a patient.

Response Style:
- Start with the most relevant information from the report.
- Explain medical terms simply.
- Use bullet points when listing findings or recommendations.
- End with the standard disclaimer.
"""

    user_prompt = f"""
Uploaded Medical Report Content:
{context}

User Question: {question}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=800,
            top_p=0.9
        )
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"⚠️ Sorry, I encountered an error while analyzing your report. Please try again. ({str(e)[:100]})"