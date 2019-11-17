export class UnemploymentRankingResponse {
  lga: string;
  mean_unemp_rate: number;
  constructor(LGA: string, mean_unemp_rate: number) {
    this.lga = LGA;
    this.mean_unemp_rate = mean_unemp_rate;
  }
}
