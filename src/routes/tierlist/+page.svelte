<script lang="ts">
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { goto } from '$app/navigation';
  import { getAllVoidpets } from '$lib/data/loadVoidpets';
  import type { Voidpet } from '$lib/types';

  let voidpets: Voidpet[] = [];
  let draggedVoidpet: Voidpet | null = null;
  let draggedFromTier: string | null = null;

  // Tier list structure
  const tiers = ['SS', 'S', 'A', 'B', 'C'];
  let tierLists: Record<string, Voidpet[]> = {
    SS: [],
    S: [],
    A: [],
    B: [],
    C: [],
    unranked: []
  };

  // Base62 encoding/decoding
  const BASE62_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz';

  function encodeBase62(str: string): string {
    // Convert string to byte array
    const bytes = new TextEncoder().encode(str);
    
    // Convert bytes to BigInt
    let num = 0n;
    for (let i = 0; i < bytes.length; i++) {
      num = num * 256n + BigInt(bytes[i]);
    }
    
    // Convert BigInt to base62
    if (num === 0n) return '0';
    
    let result = '';
    while (num > 0n) {
      result = BASE62_CHARS[Number(num % 62n)] + result;
      num = num / 62n;
    }
    
    // Prefix with length to preserve leading zeros
    return bytes.length.toString(36) + '_' + result;
  }

  function decodeBase62(encoded: string): string {
    try {
      const [lengthStr, base62Str] = encoded.split('_');
      const originalLength = parseInt(lengthStr, 36);
      
      // Convert base62 to BigInt
      let num = 0n;
      for (let i = 0; i < base62Str.length; i++) {
        const char = base62Str[i];
        const value = BASE62_CHARS.indexOf(char);
        if (value === -1) throw new Error('Invalid base62 character');
        num = num * 62n + BigInt(value);
      }
      
      // Convert BigInt to bytes
      const bytes = new Uint8Array(originalLength);
      for (let i = originalLength - 1; i >= 0; i--) {
        bytes[i] = Number(num % 256n);
        num = num / 256n;
      }
      
      // Convert bytes to string
      return new TextDecoder().decode(bytes);
    } catch (e) {
      console.error('Failed to decode base62:', e);
      throw e;
    }
  }

  onMount(async () => {
    voidpets = await getAllVoidpets();
    
    // Load from URL if present
    const urlTierData = $page.url.searchParams.get('t');
    if (urlTierData) {
      loadFromUrl(urlTierData);
    } else {
      tierLists.unranked = [...voidpets];
    }
  });

  function loadFromUrl(encodedData: string) {
    try {
      // Decode base62
      const decodedString = decodeBase62(encodedData);
      const tierData = decodedString.split('|');
      const tierMap: Record<string, string[]> = {};
      
      tierData.forEach(tierEntry => {
        const [tier, ids] = tierEntry.split(':');
        tierMap[tier] = ids ? ids.split(',').filter(id => id) : [];
      });

      // Populate tiers based on decoded data
      const allTieredIds = new Set<string>();
      
      [...tiers, 'unranked'].forEach(tier => {
        if (tierMap[tier]) {
          tierLists[tier] = tierMap[tier]
            .map(id => voidpets.find(v => v.id === id))
            .filter(v => v !== undefined) as Voidpet[];
          tierMap[tier].forEach(id => allTieredIds.add(id));
        } else {
          tierLists[tier] = [];
        }
      });

      // Put any voidpets not in the URL into unranked
      const untieredVoidpets = voidpets.filter(v => !allTieredIds.has(v.id));
      tierLists.unranked = [...tierLists.unranked, ...untieredVoidpets];
    } catch (e) {
      console.error('Failed to parse tier data from URL:', e);
      tierLists.unranked = [...voidpets];
    }
  }

  function updateUrl() {
    // Encode tier structure: SS:id1,id2|S:id3,id4|A:id5|B:|C:|unranked:id6,id7
    const parts = [...tiers, 'unranked'].map(tier => {
      const ids = tierLists[tier].map(v => v.id).join(',');
      return `${tier}:${ids}`;
    });
    
    const tierString = parts.join('|');
    // Encode to base62
    const encodedData = encodeBase62(tierString);
    const url = new URL(window.location.href);
    url.searchParams.set('t', encodedData);
    
    // Update URL without reload
    goto(url.pathname + url.search, { replaceState: true, noScroll: true, keepFocus: true });
  }

  function handleDragStart(event: DragEvent, voidpet: Voidpet, tier: string) {
    draggedVoidpet = voidpet;
    draggedFromTier = tier;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'move';
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    if (event.dataTransfer) {
      event.dataTransfer.dropEffect = 'move';
    }
  }

  function handleDrop(event: DragEvent, targetTier: string) {
    event.preventDefault();
    
    if (!draggedVoidpet || !draggedFromTier) return;

    // Remove from source tier
    tierLists[draggedFromTier] = tierLists[draggedFromTier].filter(
      (v) => v.id !== draggedVoidpet.id
    );

    // Add to target tier
    if (!tierLists[targetTier].find((v) => v.id === draggedVoidpet.id)) {
      tierLists[targetTier] = [...tierLists[targetTier], draggedVoidpet];
    }

    draggedVoidpet = null;
    draggedFromTier = null;

    // Update URL after each change
    updateUrl();
  }

  function getTierColor(tier: string): string {
    const colors: Record<string, string> = {
      SS: '#ff4444',
      S: '#ff8844',
      A: '#ffdd44',
      B: '#88dd44',
      C: '#4488dd',
      unranked: '#999999'
    };
    return colors[tier] || '#999999';
  }

  function copyShareLink() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
      alert('Share link copied to clipboard!');
    });
  }
</script>

<main>
  <h1>Voidpet Tier List</h1>

  <div class="share-controls">
    <button class="share-button" on:click={copyShareLink}>
      📋 Copy Share Link
    </button>
  </div>

  <div class="tierlist-container">
    {#each tiers as tier}
      <div class="tier-row">
        <div class="tier-label" style="background-color: {getTierColor(tier)}">
          {tier}
        </div>
        <div
          class="tier-content"
          on:dragover={handleDragOver}
          on:drop={(e) => handleDrop(e, tier)}
          role="region"
          aria-label="{tier} tier"
        >
          {#each tierLists[tier] as voidpet}
            <div
              class="voidpet-item"
              draggable="true"
              on:dragstart={(e) => handleDragStart(e, voidpet, tier)}
              role="button"
              tabindex="0"
              aria-label="Drag {voidpet.name}"
            >
              <img src={voidpet.levels[3]} alt={voidpet.name} />
              <span class="voidpet-name">{voidpet.name}</span>
            </div>
          {/each}
        </div>
      </div>
    {/each}

    <div class="tier-row unranked">
      <div class="tier-label" style="background-color: {getTierColor('unranked')}">
        Unranked
      </div>
      <div
        class="tier-content"
        on:dragover={handleDragOver}
        on:drop={(e) => handleDrop(e, 'unranked')}
        role="region"
        aria-label="Unranked voidpets"
      >
        {#each tierLists.unranked as voidpet}
          <div
            class="voidpet-item"
            draggable="true"
            on:dragstart={(e) => handleDragStart(e, voidpet, 'unranked')}
            role="button"
            tabindex="0"
            aria-label="Drag {voidpet.name}"
          >
            <img src={voidpet.levels[3]} alt={voidpet.name} />
            <span class="voidpet-name">{voidpet.name}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>
</main>

<style>
  main {
    padding: 2rem;
    max-width: 1400px;
    margin: 0 auto;
  }

  h1 {
    text-align: center;
    margin-bottom: 1rem;
    font-size: 2.5rem;
  }

  .share-controls {
    display: flex;
    justify-content: center;
    margin-bottom: 2rem;
  }

  .share-button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    background-color: #4CAF50;
    color: white;
    cursor: pointer;
    transition: all 0.2s;
    font-weight: 600;
  }

  .share-button:hover {
    background-color: #45a049;
    border-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .tierlist-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .tier-row {
    display: flex;
    min-height: 100px;
    border: 2px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f9f9f9;
  }

  .tier-row.unranked {
    margin-top: 2rem;
    min-height: 150px;
  }

  .tier-label {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: bold;
    color: white;
    min-width: 100px;
    padding: 1rem;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  }

  .tier-content {
    flex: 1;
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    min-height: 100px;
    background-color: #ffffff;
  }

  .tier-content:empty::after {
    content: 'Drop voidpets here...';
    color: #999;
    font-style: italic;
    width: 100%;
    text-align: center;
  }

  .voidpet-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    width: 80px;
    padding: 0.5rem;
    background-color: #f5f5f5;
    border: 2px solid #ddd;
    border-radius: 8px;
    cursor: move;
    transition: all 0.2s;
    position: relative;
  }

  .voidpet-item:hover {
    transform: scale(1.05);
    border-color: #999;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .voidpet-item:active {
    cursor: grabbing;
    opacity: 0.7;
  }

  .voidpet-item img {
    width: 60px;
    height: 60px;
    object-fit: contain;
  }

  .voidpet-name {
    font-size: 0.7rem;
    text-align: center;
    line-height: 1.1;
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Drag over effect */
  .tier-content:has(+ :hover) {
    background-color: #e8f5e9;
  }
</style>
