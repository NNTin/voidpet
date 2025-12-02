import { writable } from 'svelte/store';
import { getAllVoidpets } from '../data/loadVoidpets';

export const voidpetsStore = writable(getAllVoidpets());
export const filtersStore = writable({
  element: null,
  rarity: null,
});
