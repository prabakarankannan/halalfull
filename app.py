import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Explicitly load environment variables
load_dotenv()

# Get API key with explicit error handling
SAMBANOVA_API_KEY = os.getenv('SAMBANOVA_API_KEY')
if not SAMBANOVA_API_KEY:
    st.error("Please set the SAMBANOVA_API_KEY in your .env file or environment variables.")
    st.stop()

# Configure OpenAI client for SambaNova
client = openai.OpenAI(
    api_key=SAMBANOVA_API_KEY,
    base_url="https://api.sambanova.ai/v1"
)

class HalalFullChatbot:
    def __init__(self):
        self.system_prompt = """You are an AI chatbot for HalalFull.com, California's leading online meat shop platform. 
        Provide helpful, professional, and courteous support focusing on:
        1. Product recommendations
        2. Order tracking
        3. Website assistance
        4. Customer support"""

    def generate_response(self, user_query):
        """Generate AI response using SambaNova"""
        try:
            response = client.chat.completions.create(
                model='Meta-Llama-3.1-8B-Instruct',
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query}
                ],
                temperature=0.1,
                top_p=0.1
            )
            return response.choices[0].message.content
        
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return "Sorry, I'm unable to process your request at the moment."

    def handle_product_search(self, query):
        """Mock product search functionality"""
        products = {
            "beef": ["Angus Beef Ribeye", "Grass-Fed Beef Tenderloin"],
            "chicken": ["Organic Whole Chicken", "Chicken Breast Fillets"],
            "lamb": ["New Zealand Lamb Chops", "Lamb Shoulder"]
        }
        
        for category, items in products.items():
            if query.lower() in category:
                return f"Matching products in {category}: {', '.join(items)}"
        
        return "No matching products found. Try a different search term."

    def handle_order_tracking(self, order_number):
        """Mock order tracking functionality"""
        orders = {
            "HF12345": {"status": "Shipped", "estimated_delivery": "2-3 days"},
            "HF67890": {"status": "Processing", "estimated_delivery": "5-7 days"}
        }
        
        return orders.get(order_number, {"status": "Order not found"})

def main():
    st.title("HalalFull Customer Support Chatbot 🥩")
    
    # Initialize chatbot
    chatbot = HalalFullChatbot()
    
    # Sidebar for additional interactions
    st.sidebar.header("Support Options")
    support_type = st.sidebar.selectbox(
        "Select Support Type",
        ["General Chat", "Product Search", "Order Tracking"]
    )
    
    # Chat interface
    if support_type == "General Chat":
        user_query = st.text_input("Ask your question:")
        if st.button("Send"):
            if user_query:
                response = chatbot.generate_response(user_query)
                st.write("🤖 Bot Response:", response)
    
    elif support_type == "Order Tracking":
        order_number = st.text_input("Enter your order number:")
        if st.button("Track Order"):
            if order_number:
                order_status = chatbot.handle_order_tracking(order_number)
                st.write("📦 Order Status:", order_status)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.info("Need more help? Contact support@halalfull.com")

if __name__ == "__main__":
    main()