<script lang="ts">
  import { onMount } from "svelte";
  import { getAllVoidpets } from "$lib/data/loadVoidpets";
  import VoidpetCard from "$lib/components/voidpets/VoidpetCard.svelte";

  let voidpets = [];
  let globalLevel: number = 3;

  onMount(async () => {
    voidpets = await getAllVoidpets();
  });

  function decreaseGlobalLevel() {
    if (globalLevel > 1) {
      globalLevel--;
    }
  }

  function increaseGlobalLevel() {
    if (globalLevel < 5) {
      globalLevel++;
    }
  }
</script>

<main>
  <h1>Voidpets</h1>
  
  <div class="global-level-controls">
    <button on:click={decreaseGlobalLevel} disabled={globalLevel === 1}> − </button>
    <span class="level-display">Level: {globalLevel}</span>
    <button on:click={increaseGlobalLevel} disabled={globalLevel === 5}> + </button>
  </div>

  <div class="voidpets-list">
    {#each voidpets as voidpet}
      <VoidpetCard
        {voidpet}
        level={globalLevel}
        showLevelControls={false}
      />
    {/each}
  </div>
</main>

<style>
  main {
    padding: 2rem;
  }

  h1 {
    text-align: center;
    margin-bottom: 2rem;
  }

  .global-level-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 8px;
  }

  button {
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: white;
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
    min-width: 150px;
    text-align: center;
  }

  .voidpets-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }
</style>
