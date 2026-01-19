import type { LayoutServerLoad } from './$types';
import { buildNavigation, getStats } from '$lib/server/dataLoader';

export const load: LayoutServerLoad = async () => {
  const navigation = buildNavigation();
  const stats = getStats();

  return {
    navigation,
    stats
  };
};
