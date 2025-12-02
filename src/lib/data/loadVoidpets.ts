export async function getAllVoidpets() {
  const response = await fetch('/data/voidpets.json');  // Path is relative to the static folder
  if (!response.ok) {
    throw new Error('Failed to fetch voidpets');
  }
  return await response.json();
}

export async function getVoidpetById(id: string) {
  const voidpets = await getAllVoidpets();  // Fetching again, could be optimized if necessary
  return voidpets.find((v) => v.id === id);
}
