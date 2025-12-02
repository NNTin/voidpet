<script lang="ts">
  import type { Voidpet } from '$lib/types';
  export let voidpet: Voidpet;
</script>

<div class="card">
  <h3>{voidpet.name}</h3>
  <img src={voidpet.levels['1']} alt="{voidpet.name} level 1" />
</div>
