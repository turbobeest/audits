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
  let expanded = $state(true); // Start expanded by default

  function formatLabel(value: string): string {
    return value
      .split(/[-_]/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  // Toggle boolean filter
  function toggleBooleanFilter(key: string, currentValue: boolean | undefined) {
    if (currentValue === true) {
      removeFilter(key as any);
    } else {
      setFilter(key as any, true);
    }
  }
</script>

<div class="bg-white rounded-lg border border-gray-200 p-4">
  <button
    onclick={() => expanded = !expanded}
    class="w-full flex items-center justify-between cursor-pointer"
  >
    <div class="flex items-center gap-2 text-sm font-medium text-gray-700">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
      </svg>
      Filters
      {#if $hasActiveFilters}
        <span class="bg-blue-100 text-blue-800 text-xs px-2 py-0.5 rounded-full">{$activeFiltersCount}</span>
      {/if}
    </div>

    <svg
      class="w-5 h-5 text-gray-400 transition-transform {expanded ? 'rotate-180' : ''}"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
    </svg>
  </button>

  {#if expanded}
    <div class="mt-4 space-y-5 animate-fade-in">

      <!-- Row 1: Status, Category, Automation -->
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
            class="block w-32 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="active">Active</option>
            <option value="planned">Planned</option>
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
            class="block w-52 px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="">All Categories</option>
            {#each filterOptions.categories as category}
              <option value={category}>{formatLabel(category)}</option>
            {/each}
          </select>
        </div>

        <!-- Audit Type -->
        <div class="space-y-1">
          <label class="text-xs font-medium text-gray-500 uppercase">Audit Type</label>
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
            <option value="fully_automated">Deterministic</option>
            <option value="non_deterministic">Non-deterministic</option>
          </select>
        </div>
      </div>

      <!-- SDLC Phase -->
      <div class="space-y-2">
        <label class="text-xs font-medium text-gray-500 uppercase">When to Run (SDLC Phase)</label>
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

      <!-- Requirements -->
      <div class="space-y-2">
        <label class="text-xs font-medium text-gray-500 uppercase">Requirements (What the audit needs)</label>
        <div class="flex flex-wrap gap-2">
          <button
            onclick={() => toggleBooleanFilter('requiresSourceCode', $filters.requiresSourceCode)}
            class="px-3 py-1.5 text-xs rounded-full border transition-colors {$filters.requiresSourceCode
              ? 'bg-slate-700 text-white border-slate-700'
              : 'bg-white text-gray-700 border-gray-300 hover:border-slate-400'}"
          >
            Source Code
          </button>
          <button
            onclick={() => toggleBooleanFilter('requiresRuntimeData', $filters.requiresRuntimeData)}
            class="px-3 py-1.5 text-xs rounded-full border transition-colors {$filters.requiresRuntimeData
              ? 'bg-slate-700 text-white border-slate-700'
              : 'bg-white text-gray-700 border-gray-300 hover:border-slate-400'}"
          >
            Runtime Data
          </button>
          <button
            onclick={() => toggleBooleanFilter('requiresProductionAccess', $filters.requiresProductionAccess)}
            class="px-3 py-1.5 text-xs rounded-full border transition-colors {$filters.requiresProductionAccess
              ? 'bg-slate-700 text-white border-slate-700'
              : 'bg-white text-gray-700 border-gray-300 hover:border-slate-400'}"
          >
            Production Access
          </button>
          <button
            onclick={() => toggleBooleanFilter('requiresTeamInput', $filters.requiresTeamInput)}
            class="px-3 py-1.5 text-xs rounded-full border transition-colors {$filters.requiresTeamInput
              ? 'bg-slate-700 text-white border-slate-700'
              : 'bg-white text-gray-700 border-gray-300 hover:border-slate-400'}"
          >
            Team Input
          </button>
        </div>
        <p class="text-[10px] text-gray-400">Click to filter for audits that require these resources</p>
      </div>

    </div>
  {/if}
</div>
