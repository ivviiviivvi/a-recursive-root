#!/bin/bash
# AI Council System - Test Runner Script
#
# Runs comprehensive test suite including:
# - Unit tests
# - Integration tests
# - Performance benchmarks
# - Code quality checks
#
# Usage: ./scripts/test.sh [suite] [options]

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_SUITE="${1:-all}"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

run_unit_tests() {
    log_info "Running unit tests..."
    pytest "$PROJECT_DIR/tests/unit" -v --tb=short
    log_success "Unit tests passed!"
}

run_integration_tests() {
    log_info "Running integration tests..."
    pytest "$PROJECT_DIR/tests/integration" -v --tb=short
    log_success "Integration tests passed!"
}

run_performance_tests() {
    log_info "Running performance benchmarks..."
    python "$PROJECT_DIR/tests/performance/benchmark.py"
    log_success "Performance tests complete!"
}

run_code_quality() {
    log_info "Running code quality checks..."

    # Check if tools are available
    if command -v pylint &> /dev/null; then
        log_info "Running pylint..."
        pylint "$PROJECT_DIR/core" "$PROJECT_DIR/automation" || true
    fi

    if command -v black &> /dev/null; then
        log_info "Checking code formatting..."
        black --check "$PROJECT_DIR" || true
    fi

    log_success "Code quality checks complete!"
}

run_coverage() {
    log_info "Running tests with coverage..."
    pytest "$PROJECT_DIR/tests" --cov="$PROJECT_DIR" --cov-report=html --cov-report=term
    log_success "Coverage report generated in htmlcov/"
}

# Main execution
main() {
    echo "=================================="
    echo "  AI Council System - Test Suite"
    echo "  Suite: $TEST_SUITE"
    echo "=================================="
    echo ""

    cd "$PROJECT_DIR"

    case "$TEST_SUITE" in
        unit)
            run_unit_tests
            ;;
        integration)
            run_integration_tests
            ;;
        performance|benchmark)
            run_performance_tests
            ;;
        quality)
            run_code_quality
            ;;
        coverage)
            run_coverage
            ;;
        all)
            run_unit_tests
            run_integration_tests
            run_code_quality
            ;;
        *)
            echo "Unknown test suite: $TEST_SUITE"
            echo "Available suites: unit, integration, performance, quality, coverage, all"
            exit 1
            ;;
    esac

    echo ""
    log_success "Testing complete! ✅"
}

main "$@"
