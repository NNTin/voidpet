export async function getAllVoidpets() {
  const response = await fetch('/data/voidpets.json');
  if (!response.ok) {
    throw new Error('Failed to fetch voidpets');
  }
  return await response.json();
}

export async function getVoidpetById(id: string) {
  const voidpets = await getAllVoidpets();
  return voidpets.find((v) => v.id === id);
}
