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
</script>

<div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
  <!-- Total -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-gray-900">{stats.total}</div>
    <div class="text-sm text-gray-500">Total Audits</div>
  </div>

  <!-- Active -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-emerald-600">{stats.active}</div>
    <div class="text-sm text-gray-500">Active</div>
  </div>

  <!-- Planned -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-amber-600">{stats.planned}</div>
    <div class="text-sm text-gray-500">Planned</div>
  </div>

  <!-- Categories -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-blue-600">{stats.categories}</div>
    <div class="text-sm text-gray-500">Categories</div>
  </div>

  <!-- Fully Automated -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-green-600">{stats.byAutomation.fullyAutomated}</div>
    <div class="text-sm text-gray-500">Automated</div>
  </div>

  <!-- Human Required -->
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="text-2xl font-bold text-orange-600">{stats.byAutomation.humanRequired}</div>
    <div class="text-sm text-gray-500">Manual</div>
  </div>
</div>

<!-- Tier breakdown -->
<div class="mt-4 bg-white rounded-lg border border-gray-200 p-4">
  <h3 class="text-sm font-medium text-gray-700 mb-3">By Complexity Tier</h3>
  <div class="flex gap-4">
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-green-500"></span>
      <span class="text-sm text-gray-600">Focused: {stats.byTier.focused}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-blue-500"></span>
      <span class="text-sm text-gray-600">Expert: {stats.byTier.expert}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-purple-500"></span>
      <span class="text-sm text-gray-600">PhD: {stats.byTier.phd}</span>
    </div>
    <div class="flex items-center gap-2">
      <span class="w-3 h-3 rounded-full bg-gray-400"></span>
      <span class="text-sm text-gray-600">Standard: {stats.byTier.standard}</span>
    </div>
  </div>
</div>
