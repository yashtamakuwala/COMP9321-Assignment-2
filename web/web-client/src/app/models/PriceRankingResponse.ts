export class PriceRankingResponse {
  lga: string;
  mean_price: number;
  constructor(LGA: string, mean_price: number) {
    this.lga = LGA;
    this.mean_price = mean_price;
  }
}
