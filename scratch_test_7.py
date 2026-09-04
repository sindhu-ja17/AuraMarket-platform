from ai_engine import SmartChatbot
import sys

chatbot = SmartChatbot()

print("Client:", chatbot.client)

try:
    reply = chatbot.generate_reply(
        message="can you tell about the fabric of the cloth",
        is_seller_replying=True,
        product_price=100.0,
        product_info={"title": "Floral Print Maxi Dress", "description": "Beautiful dress", "category_name": "Clothing"},
        history=[{"sender_id": 1, "text": "hi"}],
        seller_id=2
    )
    print("Reply:", reply)
except Exception as e:
    print("Test Script Error:", e)
    
sys.stdout.flush()
