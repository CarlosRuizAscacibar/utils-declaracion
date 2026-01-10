# Frontend Testing Guide

This directory contains comprehensive tests for the vanilla JS frontend.

## Test Structure

```
tests/
├── frontend/                # Frontend tests
│   ├── integration/          # Integration tests (Vitest + jsdom)
│   │   ├── Application.test.js
│   │   ├── CarteraScreen.test.js
│   │   ├── YearReport.test.js
│   │   └── DiferentesAcciones.test.js
│   ├── e2e/                 # E2E tests (Playwright)
│   │   └── frontend.spec.js
│   ├── fixtures/             # Mock data and HTML
│   │   ├── mockData.js
│   │   └── testHTML.js
│   ├── setup.js              # Test setup
│   ├── mockFetch.js          # Fetch mocking utilities
│   └── domHelpers.js        # DOM manipulation helpers
├── servicios/               # Python backend tests
└── loader/                  # Data loader tests

static/
└── main.js                 # Main application code
tests/frontend/
├── vitest.config.js        # Vitest configuration
├── playwright.config.js     # Playwright configuration
└── package.json            # Dependencies and scripts
```

## Installation

```bash
cd tests/frontend
npm install
```

## Running Tests

### Integration Tests (Vitest)

```bash
# Run all integration tests
npm test

# Run tests in watch mode
npm run test:run

# Run tests with UI
npm run test:ui

# Generate coverage report
npm run test:coverage
```

### E2E Tests (Playwright)

```bash
# Run all E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in headed mode (show browser)
npm run test:e2e:headed

# Run all tests (integration + E2E)
npm run test:all
```

## Test Coverage

### Integration Tests

- **Application**: Screen registration, URL synchronization, screen display, state management
- **CarteraScreen**: Data loading, error handling, rendering operations, compra-ventas, dividendos
- **YearReport**: Year report rendering, table displays, empty data handling
- **DiferentesAcciones**: Stock list rendering, link generation, error handling

### E2E Tests

- Page navigation and routing
- URL parameter handling
- Loading states
- Error states
- Responsive design (mobile, tablet, desktop)
- Accessibility checks
- Browser compatibility (Chrome, Firefox, Safari)

## Writing New Tests

### Integration Tests

1. Create a new test file in `tests/integration/`
2. Import necessary utilities:
   ```javascript
   import { describe, it, expect, beforeEach, afterEach } from 'vitest'
   import { createScreenElement, mockURL } from '../domHelpers.js'
   import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
   ```

3. Write your test cases

### E2E Tests

1. Create a new test file in `tests/e2e/`
2. Import Playwright:
   ```javascript
   import { test, expect } from '@playwright/test'
   ```

3. Write your E2E test cases

## Mock Data

Mock data is stored in `tests/fixtures/mockData.js`. Add new fixtures here for testing different scenarios.

## Troubleshooting

### Port Already in Use

If you get a port conflict, change the port in `playwright.config.js` and update your server accordingly.

### Tests Fail to Find Elements

Ensure your HTML structure in the test matches the actual DOM. Use browser DevTools to inspect the actual structure.

### Network Requests Failing in E2E Tests

Make sure the backend server is running and the API endpoints are accessible. Update `baseURL` in `playwright.config.js` if needed.

## CI/CD Integration

These tests can be integrated into your CI/CD pipeline:

```yaml
- run: npm install
- run: npm run test:run
- run: npm run test:e2e
```
