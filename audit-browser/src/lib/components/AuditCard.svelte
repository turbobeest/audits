<script lang="ts">
  import type { AuditInventoryRow } from '$lib/types';
  import { SDLC_PHASES } from '$lib/types';

  interface Props {
    audit: AuditInventoryRow;
  }

  let { audit }: Props = $props();

  function getTierClass(tier: string): string {
    const classes: Record<string, string> = {
      focused: 'tier-focused',
      expert: 'tier-expert',
      phd: 'tier-phd',
      standard: 'tier-standard'
    };
    return classes[tier] || 'tier-standard';
  }

  function getStatusClass(status: string): string {
    return status === 'active' ? 'status-active' : 'status-planned';
  }

  // Get active SDLC phases for this audit
  let activePhases = $derived(() => {
    return SDLC_PHASES.filter(phase => {
      const key = phase.id as keyof AuditInventoryRow;
      return audit[key] === true;
    });
  });

  // Get automation info
  let automationInfo = $derived(() => {
    if (audit.fully_automated) return { label: 'Automated', color: 'text-green-600 bg-green-50' };
    if (audit.semi_automated) return { label: 'Semi-Auto', color: 'text-blue-600 bg-blue-50' };
    if (audit.human_required) return { label: 'Manual', color: 'text-orange-600 bg-orange-50' };
    return { label: 'Unknown', color: 'text-gray-600 bg-gray-50' };
  });
</script>

<div class="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-shadow">
  <div class="flex items-start justify-between gap-2 mb-2">
    <h3 class="font-medium text-gray-900 leading-tight">{audit.audit_name}</h3>
    <div class="flex gap-1.5 shrink-0">
      <span class="text-xs px-2 py-0.5 rounded-full border {getTierClass(audit.tier)}">
        {audit.tier}
      </span>
      <span class="text-xs px-2 py-0.5 rounded-full {getStatusClass(audit.status)}">
        {audit.status}
      </span>
    </div>
  </div>

  <div class="text-xs text-gray-500 mb-3">
    <span class="font-mono">{audit.audit_id}</span>
  </div>

  <div class="flex flex-wrap gap-1.5 mb-3">
    <span class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700 capitalize">
      {audit.category.replace(/-/g, ' ')}
    </span>
    <span class="text-xs px-2 py-0.5 rounded bg-gray-100 text-gray-700 capitalize">
      {audit.subcategory.replace(/-/g, ' ')}
    </span>
  </div>

  <!-- Requirements -->
  <div class="flex flex-wrap gap-1 mb-3">
    {#if audit.requires_source_code}
      <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600" title="Requires source code access">
        Source Code
      </span>
    {/if}
    {#if audit.requires_runtime_data}
      <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600" title="Requires runtime data">
        Runtime
      </span>
    {/if}
    {#if audit.requires_production_access}
      <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600" title="Requires production access">
        Production
      </span>
    {/if}
    {#if audit.requires_team_input}
      <span class="text-[10px] px-1.5 py-0.5 rounded bg-slate-100 text-slate-600" title="Requires team input">
        Team Input
      </span>
    {/if}
  </div>

  <!-- SDLC Phases (mini dots) -->
  {#if activePhases().length > 0}
    <div class="flex items-center gap-1 mb-2">
      <span class="text-[10px] text-gray-400 uppercase">SDLC:</span>
      <div class="flex gap-0.5" title={activePhases().map(p => p.label).join(', ')}>
        {#each SDLC_PHASES as phase, i}
          {@const isActive = activePhases().some(p => p.id === phase.id)}
          <span
            class="w-1.5 h-1.5 rounded-full {isActive ? 'bg-blue-500' : 'bg-gray-200'}"
            title={phase.label}
          ></span>
        {/each}
      </div>
    </div>
  {/if}

  <!-- Automation level -->
  <div class="flex items-center justify-between text-xs">
    <span class="px-2 py-0.5 rounded {automationInfo().color}">
      {automationInfo().label}
    </span>
    {#if audit.pre_production_only}
      <span class="text-gray-400">Pre-prod only</span>
    {:else if audit.production_only}
      <span class="text-gray-400">Prod only</span>
    {:else if audit.any_phase}
      <span class="text-gray-400">Any phase</span>
    {/if}
  </div>
</div>
