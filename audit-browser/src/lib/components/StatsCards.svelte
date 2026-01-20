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

  // Calculate percentages
  let automatedPercent = $derived(() => Math.round((stats.byAutomation.fullyAutomated / stats.total) * 100));
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

  <!-- Fully Automated -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-green-600">{stats.byAutomation.fullyAutomated.toLocaleString()}</div>
    <div class="text-sm text-gray-500">Fully Automated</div>
  </div>

  <!-- Manual Review -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-orange-600">{stats.byAutomation.humanRequired.toLocaleString()}</div>
    <div class="text-sm text-gray-500">Manual Review</div>
  </div>
</div>

<!-- Automation breakdown -->
<div class="mt-4 bg-white rounded-lg border border-gray-200 p-4">
  <h3 class="text-sm font-medium text-gray-700 mb-3">Automation Level Breakdown</h3>

  <!-- Progress bar -->
  <div class="h-3 rounded-full bg-gray-100 overflow-hidden flex mb-3">
    <div
      class="bg-green-500 h-full"
      style="width: {(stats.byAutomation.fullyAutomated / stats.total) * 100}%"
      title="Fully Automated: {stats.byAutomation.fullyAutomated}"
    ></div>
    <div
      class="bg-blue-500 h-full"
      style="width: {(stats.byAutomation.semiAutomated / stats.total) * 100}%"
      title="Semi-Automated: {stats.byAutomation.semiAutomated}"
    ></div>
    <div
      class="bg-orange-500 h-full"
      style="width: {(stats.byAutomation.humanRequired / stats.total) * 100}%"
      title="Manual Review: {stats.byAutomation.humanRequired}"
    ></div>
  </div>

  <div class="flex flex-wrap gap-4 text-sm">
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-green-500"></span>
      <span class="text-gray-600">Fully Automated: {stats.byAutomation.fullyAutomated.toLocaleString()}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-blue-500"></span>
      <span class="text-gray-600">Semi-Automated: {stats.byAutomation.semiAutomated.toLocaleString()}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-orange-500"></span>
      <span class="text-gray-600">Manual Review: {stats.byAutomation.humanRequired.toLocaleString()}</span>
    </div>
  </div>
</div>
