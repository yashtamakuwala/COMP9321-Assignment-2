export class Quote {
  lga: string;
  property_type: string;
  room_type: string;
  guest_count: number;
  bed_count: number;
  constructor(LGA: string, propertyType: string, roomType: string, guestCount: number, bedCount: number) {
    this.lga = LGA;
    this.property_type = propertyType;
    this.room_type = roomType;
    this.guest_count = guestCount;
    this.bed_count = bedCount;
  }
}
