<script lang="ts">
  import type { AuditInventoryRow } from '$lib/types';

  interface Props {
    audit: AuditInventoryRow | null;
    onclose: () => void;
  }

  let { audit, onclose }: Props = $props();

  let yamlContent = $state<string | null>(null);
  let loading = $state(false);
  let error = $state<string | null>(null);

  const GITHUB_RAW_BASE = 'https://raw.githubusercontent.com/turbobeest/audits/main';
  const GITHUB_BLOB_BASE = 'https://github.com/turbobeest/audits/blob/main';

  // Fetch YAML content when audit changes
  $effect(() => {
    if (audit) {
      fetchYamlContent();
    } else {
      yamlContent = null;
      error = null;
    }
  });

  async function fetchYamlContent() {
    if (!audit) return;

    loading = true;
    error = null;
    yamlContent = null;

    try {
      const url = `${GITHUB_RAW_BASE}/${audit.file_path}`;
      const response = await fetch(url);

      if (!response.ok) {
        if (response.status === 404) {
          error = 'This audit definition has not been created yet (planned).';
        } else {
          error = `Failed to fetch: ${response.status} ${response.statusText}`;
        }
        return;
      }

      yamlContent = await response.text();
    } catch (e) {
      error = `Network error: ${e instanceof Error ? e.message : 'Unknown error'}`;
    } finally {
      loading = false;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      onclose();
    }
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onclose();
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

{#if audit}
  <!-- svelte-ignore a11y_click_events_have_key_events a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4"
    onclick={handleBackdropClick}
  >
    <div class="bg-slate-800 rounded-lg border border-slate-600 w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl">
      <!-- Header -->
      <div class="flex items-center justify-between p-4 border-b border-slate-700">
        <div>
          <h2 class="text-lg font-semibold text-slate-100">{audit.audit_name}</h2>
          <div class="text-sm text-slate-400 mt-0.5">
            <span class="capitalize">{audit.category.replace(/-/g, ' ')}</span>
            <span class="mx-1">›</span>
            <span class="capitalize">{audit.subcategory.replace(/-/g, ' ')}</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <a
            href="{GITHUB_BLOB_BASE}/{audit.file_path}"
            target="_blank"
            rel="noopener noreferrer"
            class="px-3 py-1.5 text-sm bg-slate-700 hover:bg-slate-600 text-slate-200 rounded transition-colors"
          >
            View on GitHub
          </a>
          <button
            onclick={onclose}
            class="p-1.5 hover:bg-slate-700 rounded text-slate-400 hover:text-slate-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <!-- Content -->
      <div class="flex-1 overflow-auto p-4">
        {#if loading}
          <div class="flex items-center justify-center py-12">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            <span class="ml-3 text-slate-400">Loading audit definition...</span>
          </div>
        {:else if error}
          <div class="bg-amber-900/30 border border-amber-700 rounded-lg p-4">
            <div class="flex items-start gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-amber-400 shrink-0 mt-0.5">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
              <div>
                <p class="text-amber-200">{error}</p>
                {#if audit.status === 'planned'}
                  <p class="text-slate-400 text-sm mt-2">
                    This audit is planned but the YAML file hasn't been created yet.
                    Check back later or contribute to the project!
                  </p>
                {/if}
              </div>
            </div>
          </div>
        {:else if yamlContent}
          <pre class="text-sm text-slate-300 bg-slate-900 rounded-lg p-4 overflow-x-auto font-mono leading-relaxed whitespace-pre-wrap">{yamlContent}</pre>
        {/if}
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-between p-4 border-t border-slate-700 bg-slate-800/50">
        <div class="text-xs text-slate-500">
          <code>{audit.audit_id}</code>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs px-2 py-0.5 rounded-full {audit.status === 'active' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-amber-900/50 text-amber-400'}">
            {audit.status}
          </span>
          <span class="text-xs px-2 py-0.5 rounded bg-slate-700 text-slate-300">
            {audit.tier}
          </span>
        </div>
      </div>
    </div>
  </div>
{/if}
