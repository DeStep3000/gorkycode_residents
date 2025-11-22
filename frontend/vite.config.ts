import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 4173,
    allowedHosts: ['lbchresidents.ru', 'www.lbchresidents.ru'],
},
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});