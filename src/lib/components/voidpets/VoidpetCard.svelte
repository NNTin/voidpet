<script lang="ts">
  import type { Voidpet } from "$lib/types";

  export let voidpet: Voidpet;
  export let level: number = 3;
  export let showLevelControls: boolean = true;
  export let onDecreaseLevel: () => void = () => {};
  export let onIncreaseLevel: () => void = () => {};
</script>

<div class="voidpet-card">
  <div class="class-badge" data-class={voidpet.class}>
    {voidpet.class}
  </div>
  <div class="element-badge" data-element={voidpet.element}>
    <img
      src="/assets/elements/{voidpet.element.toLowerCase()}.svg"
      alt={voidpet.element}
      class="element-icon"
    />
    {voidpet.element}
  </div>
  <h2>{voidpet.name}</h2>
  <img src={voidpet.levels[level]} alt="{voidpet.name} Level {level}" />
  {#if showLevelControls}
    <div class="level-controls">
      <button on:click={onDecreaseLevel} disabled={level === 1}> − </button>
      <span class="level-display">Level {level}</span>
      <button on:click={onIncreaseLevel} disabled={level === 5}> + </button>
    </div>
  {/if}
</div>

<style>
  .voidpet-card {
    position: relative;
    border: 1px solid #ddd;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
  }

  .class-badge {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .class-badge[data-class="Fighter"] {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }

  .class-badge[data-class="Tank"] {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  }

  .class-badge[data-class="Healer"] {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  }

  .element-badge {
    position: absolute;
    top: 0.5rem;
    left: 0.5rem;
    background: transparent;
    color: #8b5cf6;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    border: 2px solid #8b5cf6;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 0.35rem;
  }

  .element-icon {
    width: 0.75rem !important;
    height: 0.75rem !important;
    margin: 0 !important;
  }

  .element-badge[data-element="Wood"] {
    border-color: #22c55e;
    color: #22c55e;
  }

  .element-badge[data-element="Earth"] {
    border-color: #a16207;
    color: #a16207;
  }

  .element-badge[data-element="Water"] {
    border-color: #06b6d4;
    color: #06b6d4;
  }

  .element-badge[data-element="Fire"] {
    border-color: #f97316;
    color: #f97316;
  }

  .element-badge[data-element="Metal"] {
    border-color: #71717a;
    color: #71717a;
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
