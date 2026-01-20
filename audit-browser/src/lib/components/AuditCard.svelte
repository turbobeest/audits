<script lang="ts">
  import type { AuditInventoryRow } from '$lib/types';
  import { SDLC_PHASES } from '$lib/types';

  interface Props {
    audit: AuditInventoryRow;
  }

  let { audit }: Props = $props();

  // Get active SDLC phases for this audit
  let activePhases = $derived(() => {
    return SDLC_PHASES.filter(phase => {
      const key = phase.id as keyof AuditInventoryRow;
      return audit[key] === true;
    });
  });

  // Get automation info
  let automationInfo = $derived(() => {
    if (audit.fully_automated) return { label: 'Fully Automated', color: 'text-green-700 bg-green-100', icon: '⚡' };
    if (audit.semi_automated) return { label: 'Semi-Automated', color: 'text-blue-700 bg-blue-100', icon: '🔧' };
    if (audit.human_required) return { label: 'Manual Review', color: 'text-orange-700 bg-orange-100', icon: '👤' };
    return { label: 'Unknown', color: 'text-gray-600 bg-gray-100', icon: '?' };
  });

  // Get phase restriction info
  let phaseRestriction = $derived(() => {
    if (audit.pre_production_only) return { label: 'Pre-Production Only', color: 'text-purple-700 bg-purple-100' };
    if (audit.production_only) return { label: 'Production Only', color: 'text-red-700 bg-red-100' };
    if (audit.any_phase) return { label: 'Any Phase', color: 'text-gray-600 bg-gray-100' };
    return null;
  });

  // Count requirements
  let requirementsList = $derived(() => {
    const reqs = [];
    if (audit.requires_source_code) reqs.push({ label: 'Source Code', icon: '📄' });
    if (audit.requires_runtime_data) reqs.push({ label: 'Runtime Data', icon: '📊' });
    if (audit.requires_production_access) reqs.push({ label: 'Prod Access', icon: '🔐' });
    if (audit.requires_team_input) reqs.push({ label: 'Team Input', icon: '👥' });
    if (audit.requires_cost_data) reqs.push({ label: 'Cost Data', icon: '💰' });
    return reqs;
  });
</script>

<div class="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
  <!-- Header -->
  <div class="flex items-start justify-between gap-2 mb-2">
    <h3 class="font-medium text-gray-900 leading-tight">{audit.audit_name}</h3>
    <span class="text-xs px-2 py-0.5 rounded-full shrink-0 {audit.status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'bg-amber-100 text-amber-700'}">
      {audit.status}
    </span>
  </div>

  <!-- Category breadcrumb -->
  <div class="text-xs text-gray-500 mb-3 flex items-center gap-1">
    <span class="capitalize">{audit.category.replace(/-/g, ' ')}</span>
    <span class="text-gray-300">›</span>
    <span class="capitalize">{audit.subcategory.replace(/-/g, ' ')}</span>
  </div>

  <!-- Automation & Phase Restriction -->
  <div class="flex flex-wrap gap-1.5 mb-3">
    <span class="text-xs px-2 py-0.5 rounded {automationInfo().color}">
      {automationInfo().label}
    </span>
    {#if phaseRestriction()}
      <span class="text-xs px-2 py-0.5 rounded {phaseRestriction().color}">
        {phaseRestriction().label}
      </span>
    {/if}
  </div>

  <!-- Requirements -->
  {#if requirementsList().length > 0}
    <div class="mb-3">
      <div class="text-[10px] text-gray-400 uppercase mb-1">Requires</div>
      <div class="flex flex-wrap gap-1">
        {#each requirementsList() as req}
          <span class="text-[11px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
            {req.label}
          </span>
        {/each}
      </div>
    </div>
  {/if}

  <!-- SDLC Phases -->
  {#if activePhases().length > 0}
    <div>
      <div class="text-[10px] text-gray-400 uppercase mb-1">SDLC Phases</div>
      <div class="flex gap-0.5" title={activePhases().map(p => p.label).join(', ')}>
        {#each SDLC_PHASES as phase}
          {@const isActive = activePhases().some(p => p.id === phase.id)}
          <div
            class="w-2 h-2 rounded-sm {isActive ? 'bg-blue-500' : 'bg-gray-200'}"
            title={phase.label}
          ></div>
        {/each}
      </div>
      <div class="text-[10px] text-gray-400 mt-1">
        {activePhases().map(p => p.label).join(' → ')}
      </div>
    </div>
  {/if}
</div>
