export class RatingRankingResponse {
  lga: string;
  mean_rating: number;
  constructor(LGA: string, mean_rating: number) {
    this.lga = LGA;
    this.mean_rating = mean_rating;
  }
}
