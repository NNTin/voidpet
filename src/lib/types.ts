export interface Voidpet {
  id: string;
  name: string;
  class: "Fighter" | "Tank" | "Healer";
  element: "Wood" | "Earth" | "Water" | "Fire" | "Metal";
  rarity: "Unknown" | "Rare" | "Epic" | "Legendary";
  levels: {
    [key: number]: string;
  };
}