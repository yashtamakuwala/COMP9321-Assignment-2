from tahelka.insight.price_ranker import PriceRanker
from tahelka.insight.rating_ranker import RatingRanker
from tahelka.insight.crime_ranker import CrimeRanker
from tahelka.insight.unemployment_ranker import UnemploymentRanker

print(PriceRanker(limit=10, ascending=True).rank())
print(RatingRanker(limit=10, ascending=False).rank())
print(CrimeRanker(limit=-1, ascending=False).rank())
print(UnemploymentRanker(limit=20, ascending=True).rank())
