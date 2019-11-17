export class QuoteResponse {
  lower: number;
  upper: number;
  constructor(upper: number, lower: number) {
    this.lower = lower;
    this.upper = upper;
  }
}
