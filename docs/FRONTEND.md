# Frontend Documentation

## Overview

The frontend of the Stock Portfolio Manager is a static Single Page Application (SPA) built using vanilla JavaScript, HTML, and CSS. It is served directly by the Flask backend without any build process or bundling.

## Architecture

The frontend follows a simple, lightweight architecture designed for easy maintenance and performance:

- **No Framework**: Uses pure JavaScript without heavy frameworks like React or Vue.js
- **Static Assets**: All frontend files are stored in the `static/` directory
- **Server-Side Rendering**: No client-side routing; the Flask server handles all routes
- **Responsive Design**: CSS includes media queries for mobile compatibility

## File Structure

```
static/
├── index.html          # Main HTML page with navigation and content containers
├── main.js            # Application logic for data fetching, DOM manipulation, and UI updates
└── style.css          # Stylesheet for layout, typography, and responsive design
```

## Development Process

Since the frontend consists of static files, there is no compilation or build step. Development involves:

1. **Editing HTML/CSS/JS**: Modify files directly in the `static/` directory
2. **Testing**: Use the frontend test suite in `tests/frontend/`
3. **Serving**: The Flask application serves the static files automatically

## Key Components

### HTML Structure (`index.html`)
- Provides the basic page layout with containers for different views
- Includes navigation menu for switching between portfolio overview and stock details
- Contains form elements for user interactions (year selection, etc.)

### JavaScript Logic (`main.js`)
- Handles API calls to the Flask backend endpoints
- Dynamically updates the DOM based on API responses
- Manages user interactions and form submissions
- Implements basic client-side validation

### Styling (`style.css`)
- Defines responsive grid layouts for tables and forms
- Provides consistent typography and color scheme
- Includes mobile-friendly breakpoints
- Styles interactive elements (buttons, links, hover states)

## API Integration

The frontend communicates with the backend through REST API endpoints:

- `GET /diferentes_acciones` - Fetch list of stocks
- `GET /cartera/{isin}` - Get detailed stock information
- `GET /report/year/{year}` - Retrieve yearly performance reports
- `POST /backup` - Create database backup

All API calls are made using the Fetch API with proper error handling.

## Testing

This section contains comprehensive tests for the vanilla JS frontend.

### Test Structure

```
tests/
├── frontend/                # Frontend tests
│   ├── integration/          # Integration tests (Vitest + jsdom)
│   │   ├── Application.test.js
│   │   ├── CarteraScreen.test.js
│   │   ├── YearReport.test.js
│   │   ├── DiferentesAcciones.test.js
│   │   └── Backup.test.js
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

### Installation

```bash
cd tests/frontend
npm install
```

### Running Tests

#### Integration Tests (Vitest)

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

#### E2E Tests (Playwright)

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

### Test Coverage

#### Integration Tests

- **Application**: Screen registration, URL synchronization, screen display, state management
- **CarteraScreen**: Data loading, error handling, rendering operations, compra-ventas, dividendos
- **YearReport**: Year report rendering, table displays, empty data handling
- **DiferentesAcciones**: Stock list rendering, link generation, error handling
- **Backup**: Backup functionality, last backup display, API error handling

#### E2E Tests

- Page navigation and routing
- URL parameter handling
- Loading states
- Error states
- Responsive design (mobile, tablet, desktop)
- Accessibility checks
- Browser compatibility (Chrome, Firefox, Safari)

### Writing New Tests

#### Integration Tests

1. Create a new test file in `tests/integration/`
2. Import necessary utilities:
   ```javascript
   import { describe, it, expect, beforeEach, afterEach } from 'vitest'
   import { createScreenElement, mockURL } from '../domHelpers.js'
   import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
   ```

3. Write your test cases

#### E2E Tests

1. Create a new test file in `tests/e2e/`
2. Import Playwright:
   ```javascript
   import { test, expect } from '@playwright/test'
   ```

3. Write your E2E test cases

### Mock Data

Mock data is stored in `tests/fixtures/mockData.js`. Add new fixtures here for testing different scenarios.

### Troubleshooting

#### Port Already in Use

If you get a port conflict, change the port in `playwright.config.js` and update your server accordingly.

#### Tests Fail to Find Elements

Ensure your HTML structure in the test matches the actual DOM. Use browser DevTools to inspect the actual structure.

#### Network Requests Failing in E2E Tests

Make sure the backend server is running and the API endpoints are accessible. Update `baseURL` in `playwright.config.js` if needed.

### CI/CD Integration

These tests can be integrated into your CI/CD pipeline:

```yaml
- run: npm install
- run: npm run test:run
- run: npm run test:e2e
```

## Writing New Functionality

The frontend uses a modular, screen-based architecture that makes it easy to add new features. Here's how to implement new functionality:

### Adding a New Screen/View

1. **Create a new screen class** in `main.js` following this pattern:
   ```javascript
   export class NewScreen {
       constructor() {
           this.data = null
           this.loading = false
           this.error = null
           this.container = document.querySelector('[data-screen="new_screen"]')
       }

       async init() {
           // Load data from API or URL params
           this.container.style.display = 'block'
           this.setLoading(true)
           this.clearError()

           try {
               const res = await fetch('/api/new-endpoint')
               if (!res.ok) throw new Error(`HTTP ${res.status}`)
               this.data = await res.json()
               this.render()
           } catch (e) {
               this.error = e.message
               this.renderError()
           } finally {
               this.setLoading(false)
           }
       }

       setLoading(loading) {
           this.loading = loading
           const loadingEl = this.container.querySelector('.c-loading')
           if (loadingEl) loadingEl.style.display = loading ? 'block' : 'none'
       }

       setError(error) {
           this.error = error
           const errorEl = this.container.querySelector('.c-error')
           if (errorEl) {
               errorEl.textContent = error
               errorEl.style.display = 'block'
           }
       }

       clearError() {
           const errorEl = this.container.querySelector('.c-error')
           if (errorEl) {
               errorEl.textContent = ''
               errorEl.style.display = 'none'
           }
       }

       renderError() {
           this.setError(this.error)
           const contentEl = this.container.querySelector('.content')
           if (contentEl) contentEl.style.display = 'none'
       }

       render() {
           this.clearError()
           const contentEl = this.container.querySelector('.content')
           if (contentEl) contentEl.style.display = 'block'
           // Update DOM with this.data
       }
   }
   ```

2. **Register the screen** in the DOMContentLoaded event listener:
   ```javascript
   const newScreen = new NewScreen()
   app.registerScreen('new_screen', newScreen)
   ```

3. **Add HTML structure** in `index.html`:
   ```html
   <div data-screen="new_screen" style="display: none;">
       <div class="c-loading">Loading...</div>
       <div class="c-error" style="display: none;"></div>
       <div class="content">
           <!-- Your screen content here -->
       </div>
   </div>
   ```

4. **Add navigation** using data-navigate attributes:
   ```html
   <a href="#" data-navigate="new_screen">New Feature</a>
   ```

### Working with the Vanilla JS Architecture

#### Key Patterns

- **Screen Classes**: Each view is encapsulated in a class with consistent lifecycle methods
- **State Management**: Use instance variables for data, loading, and error states
- **DOM Manipulation**: Direct DOM updates in render() methods using innerHTML or createElement
- **Event Handling**: Use addEventListener for user interactions
- **API Calls**: Always use async/await with try/catch for fetch requests

#### Best Practices

- **Keep it Simple**: Avoid complex state management - use simple instance variables
- **Error Handling**: Always show user-friendly error messages
- **Loading States**: Provide visual feedback during async operations
- **Accessibility**: Use semantic HTML and proper ARIA attributes
- **Performance**: Minimize DOM manipulations, use event delegation
- **Modern JS**: Use ES6+ features (classes, async/await, template literals, arrow functions)

#### Adding Styles

- Add new CSS rules in `style.css`
- Use CSS classes prefixed with component names (e.g., `.new-feature-button`)
- Follow existing responsive design patterns
- Test on different screen sizes

#### Testing New Features

1. **Unit Tests**: Add tests for new functions in `tests/frontend/`
2. **E2E Tests**: Add Playwright tests for user workflows
3. **Manual Testing**: Test navigation, API errors, and edge cases

Example test structure:
```javascript
// tests/frontend/new-feature.test.js
import { describe, it, expect } from 'vitest'

describe('NewScreen', () => {
    it('should render data correctly', () => {
        // Test implementation
    })
})
```

#### Common Tasks

- **Adding API Calls**: Create new endpoints in Flask, then add fetch calls in screen classes
- **Form Handling**: Use preventDefault, collect form data, POST to API
- **Data Validation**: Validate on client-side before API calls
- **Real-time Updates**: Use setInterval or WebSockets if needed
- **Offline Support**: Consider service workers for caching

## Deployment

The frontend is deployed as part of the Flask application. No separate build or deployment process is required - simply start the Flask server and the static files are automatically served.