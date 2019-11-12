export class Quote {
  zip_code: number;
  property_type: string;
  room_type: string;
  guest_count: number;
  bed_count: number;
  constructor(zipCode: number, propertyType: string, roomType: string, guestCount: number, bedCount: number) {
    this.zip_code = zipCode;
    this.property_type = propertyType;
    this.room_type = roomType;
    this.guest_count = guestCount;
    this.bed_count = bedCount;
  }
}
