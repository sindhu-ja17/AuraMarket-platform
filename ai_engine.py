import re
import math
from collections import Counter

# Standard stopwords for simple NLP preprocessing
STOPWORDS = set([
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant', 'cannot', 'could',
    'couldnt', 'did', 'didnt', 'do', 'does', 'doesnt', 'doing', 'dont', 'down', 'during', 'each', 'few', 'for', 'from',
    'further', 'had', 'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed', 'hell', 'hes', 'her', 'here',
    'heres', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'hows', 'i', 'id', 'ill', 'im', 'ive', 'if', 'in',
    'into', 'is', 'isnt', 'it', 'its', 'itself', 'lets', 'me', 'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor',
    'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own',
    'same', 'shant', 'she', 'shed', 'shell', 'shes', 'should', 'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats',
    'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres', 'these', 'they', 'theyd', 'theyll',
    'theyre', 'theyve', 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'wasnt', 'we',
    'wed', 'well', 'were', 'weve', 'werent', 'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which', 'while',
    'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont', 'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve',
    'your', 'yours', 'yourself', 'yourselves'
])

def tokenize(text):
    """Normalize and tokenize text to alphanumeric lowercase words."""
    if not text:
        return []
    # Replace non-alphanumeric with spaces, then lowercase and split
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())
    return [w for w in text.split() if w]

# ==========================================
# 1. SENTIMENT ANALYZER
# ==========================================
class SentimentAnalyzer:
    def __init__(self):
        # Lexicon definition
        self.positive_lexicon = {
            'perfect': 1.0, 'outstanding': 1.0, 'pristine': 1.0, 'premium': 0.9, 'clean': 0.7, 
            'amazing': 0.9, 'durable': 0.8, 'fast': 0.7, 'original': 0.6, 'stylish': 0.7, 
            'comfortable': 0.8, 'smooth': 0.7, 'excellent': 0.9, 'great': 0.8, 'good': 0.6, 
            'love': 0.8, 'like': 0.5, 'best': 0.9, 'happy': 0.7, 'friendly': 0.7, 'honest': 0.8,
            'reliable': 0.8, 'beautiful': 0.8, 'awesome': 0.9, 'superb': 0.9, 'satisfied': 0.8,
            'trusted': 0.8, 'nice': 0.6, 'neat': 0.6, 'flawless': 1.0, 'perfectly': 0.8
        }
        self.negative_lexicon = {
            'scratch': -0.5, 'dent': -0.6, 'scratchy': -0.4, 'damaged': -0.8, 'slow': -0.5, 
            'bad': -0.7, 'poor': -0.7, 'broken': -0.9, 'fake': -0.9, 'issue': -0.5, 
            'problem': -0.6, 'dirty': -0.6, 'expensive': -0.4, 'scam': -1.0, 'warning': -0.7, 
            'fraud': -1.0, 'crack': -0.7, 'repair': -0.5, 'worn': -0.5, 'hate': -0.8, 
            'dislike': -0.6, 'worst': -1.0, 'faulty': -0.8, 'disappointed': -0.8, 'waste': -0.8,
            'useless': -0.8, 'defect': -0.7, 'defective': -0.8, 'suspicious': -0.7, 'horrible': -0.9
        }
        self.negation_words = {'not', 'no', 'never', 'without', 'neither', 'nor', 'dont', 'isnt', 'wasnt', 'cant'}
        self.booster_words = {'very', 'extremely', 'highly', 'really', 'super', 'especially', 'incredibly'}

    def analyze(self, text):
        """Analyze text and return (sentiment_score, sentiment_label)."""
        tokens = tokenize(text)
        if not tokens:
            return 0.0, "Neutral"

        score = 0.0
        word_count = 0
        negate = False
        boost = 1.0

        for i, word in enumerate(tokens):
            # Check negation from previous word(s)
            if word in self.negation_words:
                negate = True
                continue
            
            # Check boosters
            if word in self.booster_words:
                boost = 1.8
                continue

            # Score word
            word_score = 0.0
            is_sentiment = False
            if word in self.positive_lexicon:
                word_score = self.positive_lexicon[word]
                is_sentiment = True
            elif word in self.negative_lexicon:
                word_score = self.negative_lexicon[word]
                is_sentiment = True

            if is_sentiment:
                if negate:
                    word_score = -word_score
                    negate = False  # Reset negation
                
                word_score *= boost
                boost = 1.0  # Reset booster
                score += word_score
                word_count += 1
            else:
                # Reset flags if we run past normal words
                if word not in self.negation_words and word not in self.booster_words:
                    negate = False
                    boost = 1.0

        if word_count == 0:
            # Check if there are minor hints
            return 0.0, "Neutral"

        # Cap the average score between -1 and 1
        avg_score = max(-1.0, min(1.0, score / word_count))

        # Classify label
        if avg_score >= 0.5:
            label = "Highly Positive"
        elif avg_score >= 0.15:
            label = "Positive"
        elif avg_score > -0.15:
            label = "Neutral"
        elif avg_score >= -0.5:
            label = "Negative"
        else:
            label = "Highly Negative"

        return round(avg_score, 2), label

# ==========================================
# 2. CONTENT MODERATOR & FRAUD DETECTOR
# ==========================================
class ContentModerator:
    def __init__(self):
        # Suspicious toxic and scam phrases
        self.blocked_keywords = {
            'scam', 'hack', 'bypass', 'untraceable', 'wire transfer only', 'western union', 
            'gift card', 'giftcard', 'cash deposit only', 'whatsapp only', 'phishing', 
            'click here', 'verified badge', 'money double', 'cryptocurrency investment'
        }
        # Standard contact detail patterns
        self.phone_pattern = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{10}\b')
        self.email_pattern = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

    def moderate_listing(self, title, description, price, category_avg_price=None):
        """Moderate a product listing. Returns (is_flagged, reason_list)."""
        reasons = []
        full_text = f"{title} {description}".lower()

        # 1. Screen toxic / blocked phrases
        for kw in self.blocked_keywords:
            if kw in full_text:
                reasons.append(f"Contains flagged suspicious phrase: '{kw}'")

        # 2. Look for phone numbers in description (often used to bypass platform chat escrow)
        phone_matches = self.phone_pattern.findall(description)
        if phone_matches:
            reasons.append(f"Detected phone number in description: '{phone_matches[0]}'. Please use the built-in marketplace chat.")

        # 3. Look for email addresses
        email_matches = self.email_pattern.findall(description)
        if email_matches:
            reasons.append(f"Detected email address in description: '{email_matches[0]}'. Please use the built-in marketplace chat.")

        # 4. Check price anomaly if category average is available
        if category_avg_price and category_avg_price > 0:
            # Flag if price is incredibly low (1/10th) or extremely high (5x) compared to average
            if price <= (category_avg_price * 0.1):
                reasons.append(f"Price (${price}) is suspiciously low compared to category average (${round(category_avg_price, 2)}). Potential scam.")
            elif price >= (category_avg_price * 5.0):
                reasons.append(f"Price (${price}) is abnormally high compared to category average (${round(category_avg_price, 2)}). Please verify price accuracy.")

        is_flagged = len(reasons) > 0
        return is_flagged, reasons

# ==========================================
# 3. PRODUCT RECOMMENDER & SEARCH RANKER (TF-IDF)
# ==========================================
class ProductRecommender:
    def __init__(self):
        self.product_data = {}  # {id: {"title": "", "desc": "", "category": "", "tokens": [...]}}
        self.idf = {}
        self.tfidf_vectors = {}  # {id: {word: tfidf_score}}
        
    def fit(self, products):
        """
        Fits the TF-IDF model on list of products.
        products list: [{"id": 1, "title": "X", "description": "Y", "category_name": "Z"}]
        """
        self.product_data = {}
        all_tokens = []
        doc_count = len(products)
        
        if doc_count == 0:
            return

        # Tokenize and store data
        word_doc_counts = Counter()
        for p in products:
            p_text = f"{p['title']} {p['description']} {p.get('category_name', '')}"
            tokens = [t for t in tokenize(p_text) if t not in STOPWORDS]
            
            self.product_data[p['id']] = {
                'id': p['id'],
                'title': p['title'],
                'description': p['description'],
                'tokens': tokens
            }
            
            # Count document frequencies
            unique_tokens = set(tokens)
            for token in unique_tokens:
                word_doc_counts[token] += 1
                
        # Calculate IDF
        self.idf = {}
        for token, count in word_doc_counts.items():
            # Standard IDF formula with smoothing
            self.idf[token] = math.log(1 + doc_count / (1 + count))
            
        # Calculate TF-IDF vectors for each document
        self.tfidf_vectors = {}
        for pid, data in self.product_data.items():
            tokens = data['tokens']
            if not tokens:
                self.tfidf_vectors[pid] = {}
                continue
                
            tf = Counter(tokens)
            total_words = len(tokens)
            
            vector = {}
            for token, count in tf.items():
                tf_val = count / total_words
                vector[token] = tf_val * self.idf.get(token, 0.0)
                
            # Normalize vector (L2 norm)
            norm = math.sqrt(sum(v**2 for v in vector.values()))
            if norm > 0:
                vector = {k: v / norm for k, v in vector.items()}
                
            self.tfidf_vectors[pid] = vector

    def get_similar_items(self, target_id, top_n=3):
        """Get top N items similar to target_id based on Cosine Similarity."""
        if target_id not in self.tfidf_vectors:
            return []
            
        target_vec = self.tfidf_vectors[target_id]
        scores = []
        
        for pid, vec in self.tfidf_vectors.items():
            if pid == target_id:
                continue
                
            # Compute Cosine Similarity between target_vec and vec
            # Since vectors are L2 normalized, it's just the dot product!
            similarity = 0.0
            for token, val in target_vec.items():
                if token in vec:
                    similarity += val * vec[token]
                    
            if similarity > 0:
                scores.append((pid, similarity))
                
        # Sort by similarity descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

    def rank_search_results(self, query, top_n=10):
        """Rank active products according to relevance to query."""
        q_tokens = [t for t in tokenize(query) if t not in STOPWORDS]
        if not q_tokens or not self.idf:
            # Return empty or let fallback handle it
            return []
            
        # Calculate query TF-IDF vector
        q_tf = Counter(q_tokens)
        total_q_words = len(q_tokens)
        
        q_vector = {}
        for token, count in q_tf.items():
            # Only compute for tokens that have IDF
            if token in self.idf:
                tf_val = count / total_q_words
                q_vector[token] = tf_val * self.idf[token]
                
        # L2 normalize query vector
        q_norm = math.sqrt(sum(v**2 for v in q_vector.values()))
        if q_norm > 0:
            q_vector = {k: v / q_norm for k, v in q_vector.items()}
        else:
            return []
            
        # Rank document similarities
        scores = []
        for pid, vec in self.tfidf_vectors.items():
            similarity = 0.0
            for token, val in q_vector.items():
                if token in vec:
                    similarity += val * vec[token]
            if similarity > 0.05:  # Relevance threshold
                scores.append((pid, similarity))
                
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]

# ==========================================
# 4. COLLABORATIVE FILTERING RECOMMENDER
# ==========================================
def get_collaborative_recommendations(user_id, conn, top_n=4):
    """
    Generate item recommendations for user_id based on User-User Jaccard similarity.
    Fails back to popular items if the user is new (cold start) or has few interactions.
    """
    cursor = conn.cursor()
    
    # 1. Fetch user interaction profiles: {uid: set([pids])}
    cursor.execute("SELECT user_id, product_id FROM interactions WHERE type IN ('view', 'like', 'buy')")
    user_interactions = {}
    for row in cursor.fetchall():
        uid = row['user_id']
        pid = row['product_id']
        if uid not in user_interactions:
            user_interactions[uid] = set()
        user_interactions[uid].add(pid)
        
    # Get active products to make sure we only recommend active ones
    cursor.execute("SELECT id FROM products WHERE status = 'active'")
    active_product_ids = set(row['id'] for row in cursor.fetchall())
        
    # Cold Start check
    if user_id not in user_interactions or len(user_interactions[user_id]) == 0:
        # Fallback to trending/popular items (most views)
        cursor.execute("SELECT id FROM products WHERE status = 'active' ORDER BY views DESC LIMIT ?", (top_n,))
        return [row['id'] for row in cursor.fetchall()]
        
    target_profile = user_interactions[user_id]
    user_similarities = []
    
    # 2. Compute Jaccard Similarity with other users
    for other_uid, other_profile in user_interactions.items():
        if other_uid == user_id:
            continue
            
        intersection = len(target_profile.intersection(other_profile))
        union = len(target_profile.union(other_profile))
        
        if union > 0:
            similarity = intersection / union
            if similarity > 0:
                user_similarities.append((other_uid, similarity))
                
    # Sort similar users by score descending
    user_similarities.sort(key=lambda x: x[1], reverse=True)
    
    # 3. Recommend products interacting with by similar users, not seen by target user
    recommendations = {}
    for similar_uid, similarity in user_similarities:
        for pid in user_interactions[similar_uid]:
            # Must be active and not already interacted with by target user
            if pid in active_product_ids and pid not in target_profile:
                if pid not in recommendations:
                    recommendations[pid] = 0.0
                recommendations[pid] += similarity
                
    # Sort recommended items by cumulative weight
    sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
    rec_ids = [pid for pid, score in sorted_recs][:top_n]
    
    # If not enough recommendations, fill up with popular items
    if len(rec_ids) < top_n:
        fill_count = top_n - len(rec_ids)
        cursor.execute(
            "SELECT id FROM products WHERE status = 'active' AND id NOT IN ({}) ORDER BY views DESC LIMIT ?".format(
                ','.join(str(i) for i in (list(target_profile) + rec_ids)) if (list(target_profile) + rec_ids) else '0'
            ), (fill_count,)
        )
        rec_ids.extend([row['id'] for row in cursor.fetchall()])
        
    return rec_ids[:top_n]

import os
try:
    from google import genai
    from google.genai import types
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        client = None
except ImportError:
    genai = None
    client = None
    GEMINI_API_KEY = None

SELLER_SYSTEM_PROMPT = """You are a professional Seller Support Chatbot for an e-commerce marketplace.

Your job is to have a natural, helpful, and unlimited conversation with sellers.

Conversation Rules

1. Continue the conversation for as many messages as the seller wants. Never stop after 2–3 replies.
2. Understand the seller's exact question and answer specifically based on their request.
3. Do not give generic or unrelated answers.
4. Remember the context of the current conversation and use previous messages when answering follow-up questions.
5. If the seller asks a follow-up question like "How much?", "When?", "Why?", "What about my order?", understand what they are referring to from the previous conversation.
6. Ask a relevant follow-up question when required instead of ending the conversation.
7. Keep replies short, clear, friendly, and professional.
8. Use simple language that sellers can easily understand.
9. If the seller is unhappy or has a complaint, respond politely and try to solve the issue.
10. Never repeat the same response unnecessarily.

Seller Topics You Should Handle

- Product listing
- Adding/editing products
- Product images
- Product description
- Product price
- Inventory/stock
- Orders
- Order cancellation
- Returns and refunds
- Payments
- Seller earnings
- Delivery/shipping
- Discounts and offers
- Customer complaints
- Account/profile issues
- Seller verification
- Store management
- General seller support

Response Behavior

For every seller message:

- First understand the intent.
- Give a direct answer.
- Provide step-by-step instructions when necessary.
- Ask one useful follow-up question if more information is needed.
- Keep the conversation open.

Example:

Seller: "How can I add a new product?"

Bot: "You can add a new product from your Seller Dashboard. Go to Products → Add Product, then enter the product name, price, description, images, and stock quantity. Finally, tap Publish.

Would you like me to guide you through adding the product step by step?"

Seller: "Yes"

Bot: "Sure! First, open Products from your dashboard and tap Add Product. What type of product are you adding?"

Seller: "Shoes"

Bot: "Great. Enter the shoe name first, then select the category, size options, color, price, and available stock. You can also upload multiple product images.

Do you want help writing the product title and description?"

Important

Never end the conversation unless the seller clearly says they are done, such as "Thanks", "Bye", or "That's all."

Always behave like a real seller-support agent, not like a generic AI assistant.
"""

class SmartChatbot:
    """A Gemini-powered chatbot for marketplace negotiations."""
    def __init__(self):
        self.client = client if genai and client else None

    def generate_reply(self, message, is_seller_replying=True, product_price=None, product_info=None, history=None, seller_id=None):
        import re
        import random
        
        # Format the context for the LLM
        if self.client and is_seller_replying:
            prompt = "Product Information:\n"
            if product_info:
                prompt += f"Title: {product_info.get('title', 'Unknown')}\n"
                prompt += f"Description: {product_info.get('description', 'Unknown')}\n"
                prompt += f"Category: {product_info.get('category_name', 'Unknown')}\n"
            if product_price is not None:
                prompt += f"Price: {product_price}\n"
                
            prompt += "\nChat History:\n"
            if history:
                for msg in history:
                    sender = "Seller" if msg['sender_id'] == seller_id else "Customer"
                    prompt += f"{sender}: {msg['text']}\n"
            
            prompt += f"\nLatest Customer Message: {message}\n"
            prompt += "\nYour Reply as the Seller:\n"
            
            try:
                response = self.client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SELLER_SYSTEM_PROMPT
                    )
                )
                return response.text.strip()
            except Exception as e:
                print(f"LLM Error: {e}")
                # Fallback to rule-based if LLM fails
                pass

        # --- Rule-Based Fallback ---
        msg_lower = message.lower()
        numbers = re.findall(r'\b\d+(?:,\d+)*(?:\.\d+)?\b', msg_lower)
        offer_price = None
        if numbers:
            try:
                offer_price = float(numbers[-1].replace(',', ''))
            except:
                pass
                
        def has_keyword(keywords):
            return any(re.search(r'\b' + re.escape(w) + r'\b', msg_lower) for w in keywords)
                
        if is_seller_replying:
            if offer_price is not None:
                if product_price and offer_price >= product_price:
                    return f"I can definitely accept {offer_price}! Let's proceed with the deal."
                elif product_price and offer_price >= product_price * 0.8:
                    return f"{offer_price} sounds reasonable. We have a deal."
                elif product_price and offer_price < product_price * 0.5:
                    return f"Sorry, {offer_price} is way too low. Can you do closer to my asking price?"
                else:
                    return f"I can't do {offer_price}, but I might consider a slightly higher offer."
            
            if has_keyword(['condition', 'quality', 'new', 'used', 'damage', 'scratch', 'defect', 'nilaimai', 'epdi iruku', 'pazhasu', 'pudusu', 'udanchuruka', 'nallairuka']):
                return "The condition is exactly as described in the listing. It's been well taken care of."
            elif has_keyword(['where', 'location', 'meet', 'pickup', 'deliver', 'ship', 'enga', 'engirunthu', 'address', 'ooru']):
                return "I can ship it securely through the platform's delivery system to ensure safety for both of us."
            elif has_keyword(['real', 'fake', 'original', 'authentic', 'duplicate', 'unmai']):
                return "Yes, it is 100% authentic and original."
            elif has_keyword(['hi', 'hello', 'hey', 'available', 'vanakkam', 'bro', 'epdi', 'boss', 'machan', 'nanba']):
                return "Hi there! Yes, the item is still available. Feel free to ask any questions or make an offer."
            elif has_keyword(['thanks', 'thank you', 'ok', 'okay', 'nandri', 'sari', 'seri', 'done', 'super']):
                return "You're welcome! Let me know if you decide to buy."
            elif has_keyword(['price', 'discount', 'lower', 'cost', 'how much', 'offer', 'velai', 'evlo', 'korachu', 'kuraikka', 'rate', 'last price']):
                return "Make me a reasonable offer and I'll consider it. I'm open to slight negotiation."
            else:
                return "Thanks for your message! Let me know if you need more details about the item or if you'd like to make an offer."
        else:
            if offer_price is not None:
                return f"Would you be willing to accept {offer_price} for this item?"
            
            if has_keyword(['price', 'offer', 'deal', 'discount', 'velai', 'evlo', 'korachi']):
                return "Is the price negotiable? I'm interested but looking for a slightly better deal."
            elif has_keyword(['ship', 'deliver', 'send', 'tomorrow', 'anuppa', 'eppa varum']):
                return "How soon can you ship the item if I purchase it today?"
            elif has_keyword(['hi', 'hello', 'hey', 'available', 'bro', 'vanakkam']):
                return "Hello! I'm interested in this item. Is it still available?"
            else:
                return "I am interested in this item. Can you provide more details?"
