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

  // Get audit type - deterministic vs non-deterministic
  let auditTypeInfo = $derived(() => {
    if (audit.fully_automated) {
      return {
        label: 'Deterministic',
        color: 'text-green-400 bg-green-900/50',
        tooltip: 'Objective pass/fail criteria - results are reliable'
      };
    }
    // semi_automated or human_required = non-deterministic
    return {
      label: 'Non-deterministic',
      color: 'text-amber-400 bg-amber-900/50',
      tooltip: 'Requires interpretation - review findings critically'
    };
  });

  // Get phase restriction info
  let phaseRestriction = $derived(() => {
    if (audit.pre_production_only) return { label: 'Pre-Production Only', color: 'text-purple-400 bg-purple-900/50' };
    if (audit.production_only) return { label: 'Production Only', color: 'text-red-400 bg-red-900/50' };
    if (audit.any_phase) return { label: 'Any Phase', color: 'text-slate-400 bg-slate-700' };
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

<div class="bg-slate-800 rounded-lg border border-slate-700 p-4 hover:border-slate-600 transition-colors">
  <!-- Header -->
  <div class="flex items-start justify-between gap-2 mb-2">
    <h3 class="font-medium text-slate-100 leading-tight">{audit.audit_name}</h3>
    <span class="text-xs px-2 py-0.5 rounded-full shrink-0 {audit.status === 'active' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-amber-900/50 text-amber-400'}">
      {audit.status}
    </span>
  </div>

  <!-- Category breadcrumb -->
  <div class="text-xs text-slate-400 mb-3 flex items-center gap-1">
    <span class="capitalize">{audit.category.replace(/-/g, ' ')}</span>
    <span class="text-slate-600">›</span>
    <span class="capitalize">{audit.subcategory.replace(/-/g, ' ')}</span>
  </div>

  <!-- Audit Type & Phase Restriction -->
  <div class="flex flex-wrap gap-1.5 mb-3">
    <span
      class="text-xs px-2 py-0.5 rounded {auditTypeInfo().color}"
      title={auditTypeInfo().tooltip}
    >
      {auditTypeInfo().label}
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
      <div class="text-[10px] text-slate-500 uppercase mb-1">Requires</div>
      <div class="flex flex-wrap gap-1">
        {#each requirementsList() as req}
          <span class="text-[11px] px-1.5 py-0.5 rounded bg-slate-700 text-slate-300">
            {req.label}
          </span>
        {/each}
      </div>
    </div>
  {/if}

  <!-- SDLC Phases -->
  {#if activePhases().length > 0}
    <div>
      <div class="text-[10px] text-slate-500 uppercase mb-1">SDLC Phases</div>
      <div class="flex gap-0.5" title={activePhases().map(p => p.label).join(', ')}>
        {#each SDLC_PHASES as phase}
          {@const isActive = activePhases().some(p => p.id === phase.id)}
          <div
            class="w-2 h-2 rounded-sm {isActive ? 'bg-blue-500' : 'bg-slate-600'}"
            title={phase.label}
          ></div>
        {/each}
      </div>
      <div class="text-[10px] text-slate-500 mt-1">
        {activePhases().map(p => p.label).join(' → ')}
      </div>
    </div>
  {/if}
</div>
