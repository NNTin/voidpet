import sveltePreprocess from 'svelte-preprocess';
import adapter from '@sveltejs/adapter-static';

export default {
  kit: {
    adapter: adapter({
      fallback: 'index.html'
    }),
    paths: {
      base: '/voidpet'
    },
    prerender: {
      handleUnseenRoutes: 'ignore'
    }
  },
  preprocess: sveltePreprocess(),
};
