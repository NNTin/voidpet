<script lang="ts">
  import { onMount } from 'svelte';
  import { getVoidpetById } from '$lib/data/loadVoidpets';
  import { page } from '$app/stores';

  let voidpet = null;
  let loading = true;

  // Get the voidpet ID from the route parameters
  $: id = $page.params.id;

  // Fetch the voidpet data when mounted
  onMount(async () => {
    if (id) {
      voidpet = await getVoidpetById(id);
      loading = false;
    }
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else if voidpet}
  <main>
    <h1>{voidpet.name}</h1>
    <p>{voidpet.description}</p>
    <div>
      {#each Object.entries(voidpet.levels) as [level, svgPath]}
        <img src={svgPath} alt="{voidpet.name} Level {level}" />
      {/each}
    </div>
  </main>
{:else}
  <p>Voidpet not found</p>
{/if}

<style>
  main {
    padding: 2rem;
  }
</style>
