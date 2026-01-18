# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-18

### Added
- **MyInvestor Data Retrieval Feature**
  - New web interface screen for retrieving data from MyInvestor platform
  - Secure credential input with username/password form
  - Automated execution of both orders and movements retrieval scripts
  - Real-time status updates and error handling

- **Backend API Enhancements**
  - New `/get_investor_data` POST endpoint accepting credentials
  - Modified `get_my_investor_orders.py` and `get_my_investor_movements.py` to accept command-line arguments
  - Enhanced subprocess execution with credential passing
  - Comprehensive error handling and status reporting

- **Frontend Improvements**
  - New `InvestorDataScreen` class with form validation and API integration
  - Added navigation link and screen container in HTML
  - CSS styling for form elements and status displays
  - Responsive design for mobile and desktop

- **Testing Coverage**
  - Frontend unit tests for `InvestorDataScreen` (16 test cases)
  - Frontend e2e tests for navigation and UI interactions
  - Backend unit tests for the new API endpoint
  - All tests passing with 98 total frontend tests

### Changed
- Updated text references from "Investor Data" to "MyInvestor Data" for clarity
- Enhanced error messages to specify the MyInvestor platform
- Improved user feedback with platform-specific messaging

### Technical Details
- **Backend Scripts**: Modified to use argparse for credential input instead of interactive prompts
- **API Design**: RESTful POST endpoint with JSON request/response format
- **Security**: Credentials passed via command-line arguments to subprocess calls
- **UI/UX**: Form validation, loading states, and user-friendly error messages
- **Testing**: Comprehensive test suite covering all new functionality

## [1.0.0] - 2024-01-01

### Added
- Initial release of Stock Portfolio Manager
- Flask web application with vanilla JavaScript frontend
- Database backup functionality
- Stock portfolio tracking and reporting
- Multiple broker data import support
- Comprehensive test suite with Vitest and Playwright

### Features
- Portfolio overview with stock listings
- Individual stock detail views
- Yearly performance reports
- Database backup system
- Responsive web interface
- RESTful API design