<script lang="ts">
  interface Props {
    stats: {
      total: number;
      active: number;
      planned: number;
      byTier: {
        focused: number;
        expert: number;
        phd: number;
        standard: number;
      };
      byAutomation: {
        fullyAutomated: number;
        semiAutomated: number;
        humanRequired: number;
      };
      categories: number;
    };
  }

  let { stats }: Props = $props();

  // Calculate derived stats
  let deterministic = $derived(() => stats.byAutomation.fullyAutomated);
  let judgmentBased = $derived(() => stats.byAutomation.semiAutomated + stats.byAutomation.humanRequired);
  let activePercent = $derived(() => Math.round((stats.active / stats.total) * 100));
</script>

<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
  <!-- Total -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-gray-900">{stats.total.toLocaleString()}</div>
    <div class="text-sm text-gray-500">Total Audits</div>
  </div>

  <!-- Active -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-emerald-600">{stats.active.toLocaleString()}</div>
    <div class="text-sm text-gray-500">Active ({activePercent()}%)</div>
  </div>

  <!-- Planned -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-amber-600">{stats.planned.toLocaleString()}</div>
    <div class="text-sm text-gray-500">Planned</div>
  </div>

  <!-- Categories -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-blue-600">{stats.categories}</div>
    <div class="text-sm text-gray-500">Categories</div>
  </div>

  <!-- Deterministic -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-green-600">{deterministic().toLocaleString()}</div>
    <div class="text-sm text-gray-500">Deterministic</div>
  </div>

  <!-- Judgment-based -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-amber-600">{judgmentBased().toLocaleString()}</div>
    <div class="text-sm text-gray-500">Judgment-based</div>
  </div>
</div>

<!-- Audit Type breakdown -->
<div class="mt-4 bg-white rounded-lg border border-gray-200 p-4">
  <h3 class="text-sm font-medium text-gray-700 mb-2">Audit Type Breakdown</h3>
  <p class="text-xs text-gray-500 mb-3">
    <strong>Deterministic</strong> audits have objective pass/fail criteria.
    <strong>Judgment-based</strong> audits require interpretation — review findings critically.
  </p>

  <!-- Progress bar -->
  <div class="h-3 rounded-full bg-gray-100 overflow-hidden flex mb-3">
    <div
      class="bg-green-500 h-full"
      style="width: {(deterministic() / stats.total) * 100}%"
      title="Deterministic: {deterministic()}"
    ></div>
    <div
      class="bg-amber-500 h-full"
      style="width: {(judgmentBased() / stats.total) * 100}%"
      title="Judgment-based: {judgmentBased()}"
    ></div>
  </div>

  <div class="flex flex-wrap gap-6 text-sm">
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-green-500"></span>
      <span class="text-gray-600">Deterministic: {deterministic().toLocaleString()} ({Math.round((deterministic() / stats.total) * 100)}%)</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-amber-500"></span>
      <span class="text-gray-600">Judgment-based: {judgmentBased().toLocaleString()} ({Math.round((judgmentBased() / stats.total) * 100)}%)</span>
    </div>
  </div>
</div>
