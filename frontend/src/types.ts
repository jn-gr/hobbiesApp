// types.ts
export interface Hobby {
    id: number;
    name: string;
  }
  
  export interface User {
    id: number;
    name: string;
    email: string;
    date_of_birth: string; // ISO string (e.g., '1990-01-01')
    hobbies: Hobby[];
  }
  