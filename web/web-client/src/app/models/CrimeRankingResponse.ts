export class CrimeRankingResponse {
  lga: string;
  mean_crime_count: number;
  constructor(LGA: string, mean_crime_count: number) {
    this.lga = LGA;
    this.mean_crime_count = mean_crime_count;
  }
}
