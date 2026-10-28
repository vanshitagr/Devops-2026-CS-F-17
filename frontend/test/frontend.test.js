import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { formatCurrency, formatDate } from '../format.js';
import { APP_NAME, APP_TAGLINE, MAX_BID_MESSAGE_LENGTH } from '../config.js';
import { CATEGORIES, LOCATIONS } from '../src/constants.js';

describe('GigBoard Frontend Unit Tests', () => {

    describe('Formatting Utilities', () => {
        it('should format currency correctly in INR', () => {
            assert.equal(formatCurrency(500), '₹500');
            assert.equal(formatCurrency(1500), '₹1,500');
            assert.equal(formatCurrency(100000), '₹1,00,000');
        });

        it('should format date strings properly', () => {
            const formatted = formatDate('2026-10-28T12:00:00Z');
            assert.ok(formatted, 'Formatted date should not be empty');
            assert.ok(formatted.includes('28') || formatted.includes('Oct'), 'Should format day or month');
        });
    });

    describe('Application Configuration & Constants', () => {
        it('should have valid application metadata', () => {
            assert.equal(APP_NAME, 'GigBoard');
            assert.ok(APP_TAGLINE.includes('SKIT Jagatpura'), 'Tagline should mention SKIT Jagatpura');
            assert.equal(MAX_BID_MESSAGE_LENGTH, 500);
        });

        it('should include required gig categories', () => {
            assert.ok(Array.isArray(CATEGORIES), 'Categories must be an array');
            assert.ok(CATEGORIES.length > 0, 'Categories must have options');
            assert.ok(CATEGORIES.some(c => c.toLowerCase().includes('help') || c.toLowerCase().includes('design') || c.toLowerCase().includes('tutoring')), 'Must include common campus categories');
        });

        it('should include Jaipur campus locations', () => {
            assert.ok(Array.isArray(LOCATIONS), 'Locations must be an array');
            assert.ok(LOCATIONS.length > 0, 'Locations must not be empty');
            assert.ok(LOCATIONS.some(loc => loc.toLowerCase().includes('skit') || loc.toLowerCase().includes('jagatpura')), 'Should contain SKIT or Jagatpura locations');
        });
    });
});
