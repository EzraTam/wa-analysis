"""Module for computation of sentiment scores based on dictionaries
Data inputs are given in the bag of words form.
"""
import os
import json

path_data = path_data = os.path.join(os.path.dirname(__file__), "data")


class ComputeSentimentFromDict:
    """Compute the sentiment of a feature vector
    by means of a dict
    """

    def __init__(self, feature_vector: list[str]):

        self.feature_vector = feature_vector

        self.li_sentiment = ["sentiment_positive_scores", "sentiment_negative_scores"]

        # Load dict
        self.dict_sentiment = {}
        for nm_sent in self.li_sentiment:
            with open("data.json") as f:
                self.dict_sentiment[nm_sent] = json.load(f)

        self.score = 0
        self.polarity = ""

    def compute_sentiment_score(self):
        """Compute sentiment score by aggregating
        over positive and negative sentiment
        """
        self.score = 0

        for nm_sent in self.li_sentiment:
            for word in self.feature_vector:
                try:
                    self.score = self.score + self.dict_sentiment[nm_sent][word]
                except KeyError:
                    pass

    def compute_polarity(self):
        """Compute polarity by thresholding
        the sentiment score
        """
        if self.score > 0:
            self.polarity = "positive"
        elif self.score < 0:
            self.polarity = "negative"
        else:
            self.polarity = "neutral"
        return dict(score=self.score, polarity=self.polarity)
