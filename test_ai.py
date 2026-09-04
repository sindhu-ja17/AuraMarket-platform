import unittest
from ai_engine import SentimentAnalyzer, ContentModerator, ProductRecommender

class TestAIEngine(unittest.TestCase):
    def setUp(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.moderator = ContentModerator()
        self.recommender = ProductRecommender()

    def test_sentiment_analysis_positive(self):
        text = "Outstanding phone! The seller was very honest and helpful. Pristine condition, highly recommended!"
        score, label = self.sentiment_analyzer.analyze(text)
        print(f"Positive Sentiment: score={score}, label={label}")
        self.assertGreater(score, 0.15)
        self.assertIn(label, ["Positive", "Highly Positive"])

    def test_sentiment_analysis_negative(self):
        text = "This item is broken, damaged, and dirty. Extremely bad service, a total waste of money."
        score, label = self.sentiment_analyzer.analyze(text)
        print(f"Negative Sentiment: score={score}, label={label}")
        self.assertLess(score, -0.15)
        self.assertIn(label, ["Negative", "Highly Negative"])

    def test_sentiment_analysis_neutral(self):
        text = "This is a grey couch. It has wooden legs and a fabric cover."
        score, label = self.sentiment_analyzer.analyze(text)
        print(f"Neutral Sentiment: score={score}, label={label}")
        self.assertTrue(-0.15 < score < 0.15)
        self.assertEqual(label, "Neutral")

    def test_content_moderation_toxic(self):
        title = "Double your money"
        description = "This is a verified badge upgrade or cryptocurrency investment. Wire transfer only!"
        is_flagged, reasons = self.moderator.moderate_listing(title, description, 100)
        print(f"Moderation (scam phrase): flagged={is_flagged}, reasons={reasons}")
        self.assertTrue(is_flagged)
        self.assertTrue(any("wire transfer only" in r.lower() or "suspicious phrase" in r.lower() for r in reasons))

    def test_content_moderation_contact(self):
        title = "iPhone for sale"
        description = "Send me a message at test@user.com or call 123-456-7890 if interested."
        is_flagged, reasons = self.moderator.moderate_listing(title, description, 500)
        print(f"Moderation (contact leakage): flagged={is_flagged}, reasons={reasons}")
        self.assertTrue(is_flagged)
        self.assertTrue(any("phone" in r.lower() or "email" in r.lower() for r in reasons))

    def test_content_moderation_price_anomaly(self):
        # Category average = $500. Price is $40 (suspiciously low) or $3000 (abnormally high)
        is_flagged_low, reasons_low = self.moderator.moderate_listing("Laptop", "Standard laptop", 40, category_avg_price=500)
        print(f"Moderation (low price outlier): flagged={is_flagged_low}, reasons={reasons_low}")
        self.assertTrue(is_flagged_low)
        self.assertTrue(any("low" in r.lower() for r in reasons_low))

        is_flagged_high, reasons_high = self.moderator.moderate_listing("Laptop", "Standard laptop", 3000, category_avg_price=500)
        print(f"Moderation (high price outlier): flagged={is_flagged_high}, reasons={reasons_high}")
        self.assertTrue(is_flagged_high)
        self.assertTrue(any("high" in r.lower() for r in reasons_high))

    def test_recommendation_tfidf(self):
        products = [
            {"id": 1, "title": "iPhone 14 Pro Max 256GB Purple", "description": "Latest Apple smartphone with amazing camera, battery life, and screen.", "category_name": "Electronics"},
            {"id": 2, "title": "Mid-Century Modern Sofa Couch - Grey", "description": "Super comfortable grey fabric sofa for living room, wooden legs.", "category_name": "Home & Garden"},
            {"id": 3, "title": "Canon EOS Mirrorless Camera Body", "description": "Professional 4K mirrorless camera body, lightweight with battery.", "category_name": "Electronics"},
            {"id": 4, "title": "iPhone 13 Charger & Cable", "description": "Fast charger power adapter and USB-C to lightning cable for iPhone.", "category_name": "Electronics"}
        ]
        self.recommender.fit(products)
        
        # Similar items to iPhone 14 (ID 1) should rank iPhone 13 Charger (ID 4) higher than Couch (ID 2)
        similar = self.recommender.get_similar_items(1)
        print(f"Similar items to ID 1: {similar}")
        similar_ids = [item_id for item_id, score in similar]
        self.assertIn(4, similar_ids)
        if 2 in similar_ids:
            # Couch should be less similar than the charger/camera
            couch_idx = similar_ids.index(2)
            charger_idx = similar_ids.index(4)
            self.assertGreater(charger_idx, -1)
            self.assertLess(charger_idx, couch_idx)

        # Search ranking test
        results = self.recommender.rank_search_results("grey comfort sofa")
        print(f"Search results for 'grey comfort sofa': {results}")
        self.assertTrue(len(results) > 0)
        self.assertEqual(results[0][0], 2) # Couch is top result

if __name__ == '__main__':
    unittest.main()
