import { FormControl, Validators } from '@angular/forms';

export class GuestCountValidator extends Validators {

  static validateNumber(control: FormControl) {

    if (control.value && control.value.length > 0) {
      if (control.value >= 1 && control.value <= 16) {
        return null;
      } else {
        return {invalid_characters: true};
      }
    } else {
      return null;
    }
  }
}
