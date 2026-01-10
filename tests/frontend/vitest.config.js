import { defineConfig } from 'vitest/config'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  test: {
    root: resolve(__dirname, './'),
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./setup.js'],
    include: ['integration/**/*.test.js', 'unit/**/*.test.js'],
    exclude: [
      'node_modules/',
      'e2e/',
      'fixtures/',
    ],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['../static/main.js'],
      exclude: [
        'node_modules/',
        'integration/',
        'e2e/',
        'fixtures/',
        '**/*.test.js',
        '**/*.spec.js',
      ],
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, '../static/'),
      '/@main.js': resolve(__dirname, '../static/main.js'),
    },
  },
})
