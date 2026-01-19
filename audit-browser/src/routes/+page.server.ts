import type { PageServerLoad } from './$types';
import { loadInventory } from '$lib/server/dataLoader';
import { getFilterOptions } from '$lib/server/search';

export const load: PageServerLoad = async () => {
  const audits = loadInventory();
  const filterOptions = getFilterOptions();

  return {
    audits,
    filterOptions
  };
};
