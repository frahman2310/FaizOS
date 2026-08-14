import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: ['src/__tests__/**/*.test.ts'],
    // The contract forbids network calls in the test suite. Tests use fixtures and temp
    // databases; the only live file access is READ ONLY row counting against data/faiz.db.
    testTimeout: 20000,
  },
});
