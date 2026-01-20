<script lang="ts">
  import SearchBar from '$lib/components/SearchBar.svelte';
  import FilterPanel from '$lib/components/FilterPanel.svelte';
  import AuditGrid from '$lib/components/AuditGrid.svelte';
  import StatsCards from '$lib/components/StatsCards.svelte';
  import { searchQuery, filters, hasActiveFilters, clearFilters } from '$lib/stores';

  let { data } = $props();

  let filteredAudits = $derived(() => {
    let results = data.audits;

    // Apply search query
    if ($searchQuery.trim()) {
      const query = $searchQuery.toLowerCase();
      results = results.filter(a =>
        a.audit_name.toLowerCase().includes(query) ||
        a.audit_id.toLowerCase().includes(query) ||
        a.category.toLowerCase().includes(query) ||
        a.subcategory.toLowerCase().includes(query)
      );
    }

    // Apply filters
    if ($filters.status) {
      results = results.filter(a => a.status === $filters.status);
    }
    if ($filters.category) {
      results = results.filter(a => a.category === $filters.category);
    }
    if ($filters.sdlcPhase) {
      const phase = $filters.sdlcPhase as keyof typeof results[0];
      results = results.filter(a => a[phase] === true);
    }
    if ($filters.automationLevel) {
      if ($filters.automationLevel === 'fully_automated') {
        results = results.filter(a => a.fully_automated);
      } else if ($filters.automationLevel === 'semi_automated') {
        results = results.filter(a => a.semi_automated);
      } else if ($filters.automationLevel === 'human_required') {
        results = results.filter(a => a.human_required);
      }
    }
    // Requirements filters
    if ($filters.requiresSourceCode) {
      results = results.filter(a => a.requires_source_code);
    }
    if ($filters.requiresRuntimeData) {
      results = results.filter(a => a.requires_runtime_data);
    }
    if ($filters.requiresProductionAccess) {
      results = results.filter(a => a.requires_production_access);
    }
    if ($filters.requiresTeamInput) {
      results = results.filter(a => a.requires_team_input);
    }

    return results;
  });
</script>

<svelte:head>
  <title>Audit Browser - Software Stack Audits</title>
</svelte:head>

<div class="space-y-6">
  <div class="flex flex-col lg:flex-row gap-4 items-start lg:items-center justify-between">
    <div>
      <h1 class="text-3xl font-bold text-gray-900">Audit Browser</h1>
      <p class="text-gray-600 mt-1">Browse and filter {data.audits.length} software stack audits</p>
    </div>
    <SearchBar />
  </div>

  <StatsCards stats={data.stats} />

  <FilterPanel filterOptions={data.filterOptions} />

  {#if $hasActiveFilters || $searchQuery}
    <div class="flex items-center gap-2 text-sm text-gray-600">
      <span>Showing {filteredAudits().length} of {data.audits.length} audits</span>
      <button
        onclick={() => clearFilters()}
        class="text-blue-600 hover:text-blue-800 underline"
      >
        Clear all filters
      </button>
    </div>
  {/if}

  <AuditGrid audits={filteredAudits()} />
</div>
