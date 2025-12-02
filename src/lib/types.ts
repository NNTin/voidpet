export interface Voidpet {
  name: string;
  class: "Fighter" | "Tank" | "Healer";
  element: "Wood" | "Earth" | "Water" | "Fire" | "Metal";
  levels: {
    [key: number]: string;
  };
}