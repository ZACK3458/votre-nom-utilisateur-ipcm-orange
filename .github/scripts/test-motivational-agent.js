#!/usr/bin/env node

// Test script for the motivational agent
console.log('🧪 Testing Motivational Agent...\n');

// Simulate different GitHub events
const testCases = [
    {
        name: 'Push Event',
        env: {
            GITHUB_EVENT_NAME: 'push',
            GITHUB_ACTOR: 'test-developer',
            GITHUB_REPOSITORY: 'test/motivational-repo',
            GITHUB_REF: 'refs/heads/main',
            COMMIT_MESSAGE: 'Add new feature for user authentication'
        }
    },
    {
        name: 'Pull Request Opened',
        env: {
            GITHUB_EVENT_NAME: 'pull_request',
            GITHUB_EVENT_ACTION: 'opened',
            GITHUB_ACTOR: 'contributor',
            GITHUB_REPOSITORY: 'test/motivational-repo',
            GITHUB_REF: 'refs/heads/feature/new-ui'
        }
    },
    {
        name: 'Pull Request Merged',
        env: {
            GITHUB_EVENT_NAME: 'pull_request',
            GITHUB_EVENT_ACTION: 'closed',
            GITHUB_ACTOR: 'lead-dev',
            GITHUB_REPOSITORY: 'test/motivational-repo',
            GITHUB_REF: 'refs/heads/feature/api-improvement',
            PR_MERGED: 'true',
            PR_STATE: 'closed'
        }
    },
    {
        name: 'Code Review',
        env: {
            GITHUB_EVENT_NAME: 'pull_request_review',
            GITHUB_EVENT_ACTION: 'submitted',
            GITHUB_ACTOR: 'senior-dev',
            GITHUB_REPOSITORY: 'test/motivational-repo'
        }
    }
];

async function runTest(testCase) {
    console.log(`\n🔍 Testing: ${testCase.name}`);
    console.log('=' .repeat(50));
    
    // Set environment variables
    Object.keys(testCase.env).forEach(key => {
        process.env[key] = testCase.env[key];
    });
    
    try {
        // Import and run the motivational agent
        delete require.cache[require.resolve('./motivational-agent.js')];
        await require('./motivational-agent.js');
        console.log(`✅ ${testCase.name} completed successfully`);
    } catch (error) {
        console.error(`❌ ${testCase.name} failed:`, error.message);
    }
    
    // Clean up environment variables
    Object.keys(testCase.env).forEach(key => {
        delete process.env[key];
    });
}

async function runAllTests() {
    console.log('🚀 Running all test cases...\n');
    
    for (const testCase of testCases) {
        await runTest(testCase);
    }
    
    console.log('\n🎉 All tests completed!');
}

// Run tests if this script is executed directly
if (require.main === module) {
    runAllTests().catch(console.error);
}

module.exports = { runAllTests, runTest };