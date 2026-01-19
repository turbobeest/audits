<script lang="ts">
  import type { NavCategory } from '$lib/types';
  import { toggleCategory, toggleSubcategory, expandedCategories, expandedSubcategories, setFilter } from '$lib/stores';
  import { CATEGORY_CLUSTERS } from '$lib/types';

  interface Props {
    navigation: NavCategory[];
  }

  let { navigation }: Props = $props();

  function getCategoryCluster(categoryNumber: number): string {
    for (const [name, config] of Object.entries(CATEGORY_CLUSTERS)) {
      if (categoryNumber >= config.range[0] && categoryNumber <= config.range[1]) {
        return name;
      }
    }
    return 'Core Technical';
  }

  function getClusterColor(cluster: string): string {
    const colors: Record<string, string> = {
      'Core Technical': 'border-l-blue-500',
      'Infrastructure': 'border-l-green-500',
      'Human & Experience': 'border-l-purple-500',
      'Process & Governance': 'border-l-orange-500',
      'Economics & Dependencies': 'border-l-yellow-500',
      'Specialized Domains': 'border-l-red-500'
    };
    return colors[cluster] || 'border-l-gray-500';
  }

  function getTierColor(tier: string): string {
    const colors: Record<string, string> = {
      focused: 'bg-green-500',
      expert: 'bg-blue-500',
      phd: 'bg-purple-500',
      standard: 'bg-gray-400'
    };
    return colors[tier] || 'bg-gray-400';
  }
</script>

<aside class="w-80 bg-white border-r border-gray-200 overflow-y-auto h-[calc(100vh-73px)] sticky top-[73px]">
  <div class="p-4">
    <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Categories</h2>

    <nav class="space-y-1">
      {#each navigation as category}
        {@const cluster = getCategoryCluster(category.number)}
        {@const clusterColor = getClusterColor(cluster)}

        <div class="border-l-4 {clusterColor}">
          <button
            onclick={() => toggleCategory(category.id)}
            class="w-full flex items-center justify-between px-3 py-2 text-left hover:bg-gray-50 transition-colors"
          >
            <div class="flex items-center gap-2 min-w-0">
              <span class="text-xs font-mono text-gray-400">{category.number}.</span>
              <span class="font-medium text-gray-900 truncate">{category.title}</span>
            </div>
            <div class="flex items-center gap-2 shrink-0">
              <span class="text-xs text-gray-500 bg-gray-100 px-1.5 py-0.5 rounded">{category.auditCount}</span>
              <svg
                class="w-4 h-4 text-gray-400 transition-transform {$expandedCategories.has(category.id) ? 'rotate-90' : ''}"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </div>
          </button>

          {#if $expandedCategories.has(category.id)}
            <div class="ml-4 border-l border-gray-200">
              {#each category.subcategories as subcategory}
                <div>
                  <button
                    onclick={() => toggleSubcategory(subcategory.id)}
                    class="w-full flex items-center justify-between px-3 py-1.5 text-left text-sm hover:bg-gray-50 transition-colors"
                  >
                    <span class="text-gray-700 truncate">{subcategory.title}</span>
                    <div class="flex items-center gap-2 shrink-0">
                      <span class="text-xs text-gray-400">{subcategory.audits.length}</span>
                      <svg
                        class="w-3 h-3 text-gray-400 transition-transform {$expandedSubcategories.has(subcategory.id) ? 'rotate-90' : ''}"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </button>

                  {#if $expandedSubcategories.has(subcategory.id)}
                    <div class="ml-3 py-1">
                      {#each subcategory.audits as audit}
                        <button
                          onclick={() => setFilter('category', category.slug)}
                          class="w-full flex items-center gap-2 px-3 py-1 text-left text-xs hover:bg-gray-50 transition-colors group"
                        >
                          <span class="w-1.5 h-1.5 rounded-full {getTierColor(audit.tier)}"></span>
                          <span class="text-gray-600 truncate group-hover:text-gray-900">{audit.name}</span>
                          {#if audit.status === 'planned'}
                            <span class="text-[10px] text-amber-600 bg-amber-50 px-1 rounded">planned</span>
                          {/if}
                        </button>
                      {/each}
                    </div>
                  {/if}
                </div>
              {/each}
            </div>
          {/if}
        </div>
      {/each}
    </nav>
  </div>

  <!-- Legend -->
  <div class="p-4 border-t border-gray-200 mt-4">
    <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Tier Legend</h3>
    <div class="grid grid-cols-2 gap-2 text-xs">
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-green-500"></span>
        <span class="text-gray-600">Focused</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-blue-500"></span>
        <span class="text-gray-600">Expert</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-purple-500"></span>
        <span class="text-gray-600">PhD</span>
      </div>
      <div class="flex items-center gap-2">
        <span class="w-2 h-2 rounded-full bg-gray-400"></span>
        <span class="text-gray-600">Standard</span>
      </div>
    </div>
  </div>
</aside>
