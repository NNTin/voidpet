<script lang="ts">
  import { onMount } from 'svelte';
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

  onMount(async () => {
    voidpets = await getAllVoidpets();
    tierLists.unranked = [...voidpets];
  });

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
</script>

<main>
  <h1>Voidpet Tier List</h1>

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
    margin-bottom: 2rem;
    font-size: 2.5rem;
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
