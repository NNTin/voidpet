<script lang="ts">
  import { onMount } from 'svelte';
  import { getAllVoidpets } from '$lib/data/loadVoidpets';

  let voidpets = [];
  let levels: { [key: string]: number } = {};

  onMount(async () => {
    voidpets = await getAllVoidpets();
    // Initialize all voidpets to level 3
    voidpets.forEach((voidpet) => {
      levels[voidpet.id] = 3;
    });
  });

  function decreaseLevel(id: string) {
    if (levels[id] > 1) {
      levels[id]--;
    }
  }

  function increaseLevel(id: string) {
    if (levels[id] < 5) {
      levels[id]++;
    }
  }
</script>

<main>
  <h1>Voidpets</h1>
  <div class="voidpets-list">
    {#each voidpets as voidpet}
      <div class="voidpet-card">
        <h2>{voidpet.name}</h2>
        <img src={voidpet.levels[levels[voidpet.id]]} alt="{voidpet.name} Level {levels[voidpet.id]}" />
        <div class="level-controls">
          <button on:click={() => decreaseLevel(voidpet.id)} disabled={levels[voidpet.id] === 1}>
            −
          </button>
          <span class="level-display">Level {levels[voidpet.id]}</span>
          <button on:click={() => increaseLevel(voidpet.id)} disabled={levels[voidpet.id] === 5}>
            +
          </button>
        </div>
      </div>
    {/each}
  </div>
</main>

<style>
  .voidpets-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }

  .voidpet-card {
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
  }

  .voidpet-card img {
    width: 100%;
    max-width: 150px;
    height: auto;
    margin: 0.5rem 0;
  }

  .level-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  button {
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f5f5f5;
    cursor: pointer;
    transition: all 0.2s;
  }

  button:hover:not(:disabled) {
    background-color: #e0e0e0;
    border-color: #999;
  }

  button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .level-display {
    font-weight: bold;
    min-width: 80px;
  }
</style>
