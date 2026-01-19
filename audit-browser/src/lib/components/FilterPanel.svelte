<script lang="ts">
  import { filters, setFilter, removeFilter, hasActiveFilters, activeFiltersCount } from '$lib/stores';
  import { SDLC_PHASES } from '$lib/types';

  interface Props {
    filterOptions: {
      categories: string[];
      tiers: readonly string[];
      statuses: readonly string[];
      automationLevels: readonly string[];
    };
  }

  let { filterOptions }: Props = $props();
  let expanded = $state(false);

  function formatLabel(value: string): string {
    return value
      .split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
</script>

<div class="bg-white rounded-lg border border-gray-200 p-4">
  <div class="flex items-center justify-between">
    <button
      onclick={() => expanded = !expanded}
      class="flex items-center gap-2 text-sm font-medium text-gray-700"
    >
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
      </svg>
      Filters
      {#if $hasActiveFilters}
        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">{$activeFiltersCount}</span>
      {/if}
    </button>

    <svg
      class="w-5 h-5 text-gray-400 transition-transform {expanded ? 'rotate-180' : ''}"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </div>

  {#if expanded}
    <div class="mt-4 space-y-4 animate-fade-in">
      <!-- Quick filters row -->
      <div class="flex flex-wrap gap-4">
        <!-- Status -->
        <div class="space-y-1">
          <label class="text-xs font-medium text-gray-500 uppercase">Status</label>
          <select
            value={$filters.status || ''}
            onchange={(e) => {
              const value = (e.target as HTMLSelectElement).value;
              if (value) setFilter('status', value as 'active' | 'planned');
              else removeFilter('status');
            }}
            class="block w-36 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            {#each filterOptions.statuses as status}
              <option value={status}>{formatLabel(status)}</option>
            {/each}
          </select>
        </div>

        <!-- Tier -->
        <div class="space-y-1">
          <label class="text-xs font-medium text-gray-500 uppercase">Tier</label>
          <select
            value={$filters.tier || ''}
            onchange={(e) => {
              const value = (e.target as HTMLSelectElement).value;
              if (value) setFilter('tier', value as any);
              else removeFilter('tier');
            }}
            class="block w-36 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            {#each filterOptions.tiers as tier}
              <option value={tier}>{formatLabel(tier)}</option>
            {/each}
          </select>
        </div>

        <!-- Category -->
        <div class="space-y-1">
          <label class="text-xs font-medium text-gray-500 uppercase">Category</label>
          <select
            value={$filters.category || ''}
            onchange={(e) => {
              const value = (e.target as HTMLSelectElement).value;
              if (value) setFilter('category', value);
              else removeFilter('category');
            }}
            class="block w-48 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Categories</option>
            {#each filterOptions.categories as category}
              <option value={category}>{formatLabel(category)}</option>
            {/each}
          </select>
        </div>

        <!-- Automation Level -->
        <div class="space-y-1">
          <label class="text-xs font-medium text-gray-500 uppercase">Automation</label>
          <select
            value={$filters.automationLevel || ''}
            onchange={(e) => {
              const value = (e.target as HTMLSelectElement).value;
              if (value) setFilter('automationLevel', value as any);
              else removeFilter('automationLevel');
            }}
            class="block w-44 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            {#each filterOptions.automationLevels as level}
              <option value={level}>{formatLabel(level)}</option>
            {/each}
          </select>
        </div>
      </div>

      <!-- SDLC Phase -->
      <div class="space-y-2">
        <label class="text-xs font-medium text-gray-500 uppercase">SDLC Phase</label>
        <div class="flex flex-wrap gap-2">
          {#each SDLC_PHASES as phase}
            <button
              onclick={() => {
                if ($filters.sdlcPhase === phase.id) {
                  removeFilter('sdlcPhase');
                } else {
                  setFilter('sdlcPhase', phase.id);
                }
              }}
              class="px-3 py-1.5 text-xs rounded-full border transition-colors {$filters.sdlcPhase === phase.id
                ? 'bg-blue-500 text-white border-blue-500'
                : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400'}"
              title={phase.description}
            >
              {phase.label}
            </button>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</div>
