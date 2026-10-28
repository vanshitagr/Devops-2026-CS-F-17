import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import jwt from 'jsonwebtoken';
import bcrypt from 'bcryptjs';
import User from '../models/User.js';
import Gig from '../models/Gig.js';
import Bid from '../models/Bid.js';
import client from 'prom-client';

describe('GigBoard Backend Unit Tests', () => {

    describe('Prometheus Metrics Integration', () => {
        it('should have collectDefaultMetrics registered', async () => {
            client.collectDefaultMetrics();
            const metrics = await client.register.metrics();
            assert.ok(metrics, 'Prometheus metrics string should not be empty');
            assert.ok(metrics.includes('process_cpu_') || metrics.includes('nodejs_'), 'Should contain nodejs / process default metrics');
        });

        it('should have correct content type for Prometheus exporter', () => {
            assert.ok(client.register.contentType.includes('text/plain'), 'Content-Type should be Prometheus standard');
        });
    });

    describe('User Model Schema Validation', () => {
        it('should require name field', async () => {
            const user = new User({ email: 'test@skit.ac.in', password: 'password123' });
            let err = null;
            try { await user.validate(); } catch (e) { err = e; }
            assert.ok(err, 'Expected validation error for missing name');
            assert.ok(err.errors.name, 'Expected error on name field');
        });

        it('should require email field', async () => {
            const user = new User({ name: 'Vanshita', password: 'password123' });
            let err = null;
            try { await user.validate(); } catch (e) { err = e; }
            assert.ok(err, 'Expected validation error for missing email');
            assert.ok(err.errors.email, 'Expected error on email field');
        });

        it('should reject password shorter than 6 characters', async () => {
            const user = new User({ name: 'Vanshita', email: 'test@skit.ac.in', password: '123' });
            let err = null;
            try { await user.validate(); } catch (e) { err = e; }
            assert.ok(err, 'Expected validation error for short password');
            assert.ok(err.errors.password, 'Expected error on password field');
        });

        it('should default college to SKIT Jagatpura, Jaipur', () => {
            const user = new User({ name: 'Student', email: 'student@skit.ac.in', password: 'password123' });
            assert.equal(user.college, 'SKIT Jagatpura, Jaipur');
        });

        it('should correctly hash and match password using bcrypt', async () => {
            const plainPassword = 'securePassword123';
            const salt = await bcrypt.genSalt(10);
            const hashedPassword = await bcrypt.hash(plainPassword, salt);
            const isMatch = await bcrypt.compare(plainPassword, hashedPassword);
            assert.equal(isMatch, true, 'Password comparison should match');
        });

        it('should generate valid JWT tokens', () => {
            const secret = 'test-devops-jwt-secret';
            const payload = { id: 'mock-user-id-123' };
            const token = jwt.sign(payload, secret, { expiresIn: '1d' });
            const decoded = jwt.verify(token, secret);
            assert.equal(decoded.id, 'mock-user-id-123');
        });
    });

    describe('Gig Model Schema Validation', () => {
        it('should require title, description, category, and budget', async () => {
            const gig = new Gig({});
            let err = null;
            try { await gig.validate(); } catch (e) { err = e; }
            assert.ok(err, 'Expected validation error for empty Gig');
            assert.ok(err.errors.title, 'Expected title required error');
            assert.ok(err.errors.description, 'Expected description required error');
            assert.ok(err.errors.category, 'Expected category required error');
            assert.ok(err.errors.budget, 'Expected budget required error');
        });

        it('should default status to open', () => {
            const gig = new Gig({
                title: 'Help shifting room',
                description: 'Need help moving books and luggage to new hostel room',
                category: 'moving',
                budget: 500,
                location: 'Hostel Block A',
                deadline: new Date(),
                postedBy: '507f1f77bcf86cd799439011'
            });
            assert.equal(gig.status, 'open');
        });
    });

    describe('Bid Model Schema Validation', () => {
        it('should require gig, bidder, and amount', async () => {
            const bid = new Bid({});
            let err = null;
            try { await bid.validate(); } catch (e) { err = e; }
            assert.ok(err, 'Expected validation error for empty Bid');
            assert.ok(err.errors.gig, 'Expected gig required error');
            assert.ok(err.errors.bidder, 'Expected bidder required error');
            assert.ok(err.errors.amount, 'Expected amount required error');
        });

        it('should default status to pending', () => {
            const bid = new Bid({
                gig: '507f1f77bcf86cd799439011',
                bidder: '507f1f77bcf86cd799439012',
                amount: 450,
                message: 'I can do this today after 5pm'
            });
            assert.equal(bid.status, 'pending');
        });
    });
});
