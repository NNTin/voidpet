<script lang="ts">
  import { onMount } from 'svelte';
  import { getAllVoidpets } from '$lib/data/loadVoidpets';

  let voidpets = [];

  onMount(async () => {
    voidpets = await getAllVoidpets();
  });
</script>

<main>
  <h1>Voidpets</h1>
  <div class="voidpets-list">
    {#each voidpets as voidpet}
      <div class="voidpet-card">
        <h2>{voidpet.name}</h2>
        <img src={voidpet.levels['1']} alt="{voidpet.name} Level 1" />
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
</style>
