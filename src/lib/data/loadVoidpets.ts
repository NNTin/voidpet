export async function getAllVoidpets() {
  const base = import.meta.env.BASE_URL || ''; // Fallback to empty string if BASE_URL isn't defined
  const response = await fetch(`${base}/data/voidpets.json`);
  if (!response.ok) {
    throw new Error('Failed to fetch voidpets');
  }
  return await response.json();
}

export async function getVoidpetById(id: string) {
  const voidpets = await getAllVoidpets();
  return voidpets.find((v) => v.id === id);
}
