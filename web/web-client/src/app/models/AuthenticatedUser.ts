export class AuthenticatedUser {
  email: string;
  isAdmin: boolean;
  token: string;
  constructor(email: string, isAdmin: boolean, token: string) {
    this.email = email;
    this.isAdmin = isAdmin;
    this.token = token;
  }
}
