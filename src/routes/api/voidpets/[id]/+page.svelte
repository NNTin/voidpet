<script lang="ts">
  import { onMount } from 'svelte';
  import { getVoidpetById } from '$lib/data/loadVoidpets';
  import { page } from '$app/stores';
  import VoidpetCard from '$lib/components/voidpets/VoidpetCard.svelte';

  let voidpet = null;
  let level = 3;
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

  function decreaseLevel() {
    if (level > 1) {
      level--;
    }
  }

  function increaseLevel() {
    if (level < 5) {
      level++;
    }
  }
</script>

{#if loading}
  <main>
    <p>Loading...</p>
  </main>
{:else if voidpet}
  <main>
    <VoidpetCard
      {voidpet}
      {level}
      showLevelControls={true}
      onDecreaseLevel={decreaseLevel}
      onIncreaseLevel={increaseLevel}
    />
  </main>
{:else}
  <main>
    <p>Voidpet not found</p>
  </main>
{/if}

<style>
  main {
    padding: 2rem;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
  }
</style>
