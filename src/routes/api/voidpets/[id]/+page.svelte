<script lang="ts">
  import { getVoidpetById } from '$lib/data/loadVoidpets';
  import { page } from '$app/stores';

  let voidpet;

  // Get the voidpet ID from the route parameters
  $: id = $page.params.id;

  // Fetch the voidpet data when the ID changes
  $: {
    if (id) {
      voidpet = getVoidpetById(id);
    }
  }
</script>

{#if voidpet}
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
  <p>Loading...</p>
{/if}

<style>
  main {
    padding: 2rem;
  }
</style>
