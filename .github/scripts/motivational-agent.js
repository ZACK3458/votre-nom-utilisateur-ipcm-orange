#!/usr/bin/env node

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration from environment variables
const config = {
    slackWebhookUrl: process.env.SLACK_WEBHOOK_URL,
    githubToken: process.env.GITHUB_TOKEN,
    eventName: process.env.GITHUB_EVENT_NAME,
    eventAction: process.env.GITHUB_EVENT_ACTION,
    actor: process.env.GITHUB_ACTOR,
    ref: process.env.GITHUB_REF,
    repository: process.env.GITHUB_REPOSITORY,
    prMerged: process.env.PR_MERGED === 'true',
    prState: process.env.PR_STATE,
    commitMessage: process.env.COMMIT_MESSAGE
};

// Motivational messages in French
const motivationalMessages = {
    push: [
        "Excellent travail sur ce commit ! 🚀 Continue comme ça, tu es sur la bonne voie !",
        "Superbe commit ! 💪 Chaque ligne de code nous rapproche du succès !",
        "Bravo pour ce push ! 🎉 Ta détermination porte ses fruits !",
        "Fantastique ! 🌟 Ce commit montre ton engagement et ta qualité de travail !",
        "Formidable ! 👏 Continue à coder avec cette passion !"
    ],
    pullRequestOpened: [
        "Excellente PR ! 🎯 Ta contribution va faire la différence !",
        "Superbe pull request ! 🔥 L'équipe va adorer ton travail !",
        "Bravo pour cette PR ! 💡 Tes idées sont toujours pertinentes !",
        "Fantastique contribution ! 🚀 Continue à proposer d'excellentes améliorations !",
        "Magnifique travail ! ✨ Cette PR montre ton expertise !"
    ],
    pullRequestMerged: [
        "Pull request fusionnée ! 🎉 Allez, passe à la prochaine fonctionnalité !",
        "Merge réussi ! 🚀 Ton code est maintenant en production, félicitations !",
        "Parfait ! 💯 Une autre feature de qualité qui rejoint la base de code !",
        "Excellent ! 🌟 Ton travail améliore constamment notre projet !",
        "Bravo ! 🏆 Cette fusion marque encore un succès dans ton parcours !"
    ],
    pullRequestClosed: [
        "Pas de souci pour cette PR ! 💪 Chaque tentative nous rapproche de la perfection !",
        "Continue ! 🚀 Les meilleures idées naissent souvent après plusieurs essais !",
        "Garde le cap ! ⭐ Ton prochain PR sera encore meilleur !",
        "Excellent esprit ! 🔥 L'innovation nécessite parfois plusieurs itérations !",
        "Persévère ! 💡 Tes efforts constants mènent toujours au succès !"
    ],
    review: [
        "Merci pour cette review ! 👀 Ton œil expert améliore la qualité du code !",
        "Excellente review ! 🔍 Tes commentaires sont toujours constructifs !",
        "Superbe analyse ! 💡 Ton feedback aide toute l'équipe à progresser !",
        "Bravo pour cette review ! 🎯 Ta rigueur est précieuse pour le projet !",
        "Merci ! 🙏 Tes reviews maintiennent nos standards de qualité élevés !"
    ]
};

function getRandomMessage(messageArray) {
    return messageArray[Math.floor(Math.random() * messageArray.length)];
}

function analyzeEventAndGenerateMessage() {
    let message = "";
    let emoji = "🎉";
    
    console.log(`Analyzing event: ${config.eventName} with action: ${config.eventAction}`);
    
    switch (config.eventName) {
        case 'push':
            message = getRandomMessage(motivationalMessages.push);
            emoji = "🚀";
            break;
            
        case 'pull_request':
            if (config.eventAction === 'opened') {
                message = getRandomMessage(motivationalMessages.pullRequestOpened);
                emoji = "🎯";
            } else if (config.eventAction === 'closed' && config.prMerged) {
                message = getRandomMessage(motivationalMessages.pullRequestMerged);
                emoji = "🎉";
            } else if (config.eventAction === 'closed') {
                message = getRandomMessage(motivationalMessages.pullRequestClosed);
                emoji = "💪";
            }
            break;
            
        case 'pull_request_review':
            if (config.eventAction === 'submitted') {
                message = getRandomMessage(motivationalMessages.review);
                emoji = "👀";
            }
            break;
            
        default:
            message = `Excellent travail ${config.actor} ! 🌟 Continue ton super boulot !`;
            emoji = "⭐";
    }
    
    return { message, emoji };
}

function formatSlackMessage(motivationalContent) {
    const branchName = config.ref ? config.ref.replace('refs/heads/', '') : 'unknown';
    const commitMsg = config.commitMessage ? config.commitMessage.substring(0, 100) + '...' : '';
    
    return {
        text: `${motivationalContent.emoji} Motivation GitHub`,
        blocks: [
            {
                type: "header",
                text: {
                    type: "plain_text",
                    text: `${motivationalContent.emoji} Agent Motivationnel`
                }
            },
            {
                type: "section",
                text: {
                    type: "mrkdwn",
                    text: `*${motivationalContent.message}*`
                }
            },
            {
                type: "context",
                elements: [
                    {
                        type: "mrkdwn",
                        text: `👤 *${config.actor}* | 📁 *${config.repository}* | 🌿 *${branchName}*`
                    }
                ]
            }
        ]
    };
}

function sendSlackNotification(messageData) {
    return new Promise((resolve, reject) => {
        if (!config.slackWebhookUrl) {
            console.log('No Slack webhook URL configured. Message would be:');
            console.log(JSON.stringify(messageData, null, 2));
            resolve(true);
            return;
        }
        
        const url = new URL(config.slackWebhookUrl);
        const postData = JSON.stringify(messageData);
        
        const options = {
            hostname: url.hostname,
            port: url.port || 443,
            path: url.pathname,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(postData)
            }
        };
        
        const req = https.request(options, (res) => {
            console.log(`Slack response status: ${res.statusCode}`);
            
            let body = '';
            res.on('data', (chunk) => {
                body += chunk;
            });
            
            res.on('end', () => {
                if (res.statusCode === 200) {
                    console.log('✅ Motivational message sent successfully to Slack!');
                    resolve(true);
                } else {
                    console.error(`❌ Failed to send message. Status: ${res.statusCode}, Body: ${body}`);
                    reject(new Error(`Slack API error: ${res.statusCode}`));
                }
            });
        });
        
        req.on('error', (error) => {
            console.error('❌ Error sending to Slack:', error);
            reject(error);
        });
        
        req.write(postData);
        req.end();
    });
}

function sendEmailNotification(messageContent) {
    // Placeholder for email functionality
    // In a real implementation, you would integrate with services like:
    // - SendGrid
    // - AWS SES
    // - Nodemailer with SMTP
    console.log('📧 Email notification (placeholder):');
    console.log(`Subject: Motivation GitHub - ${messageContent.emoji}`);
    console.log(`Body: ${messageContent.message}`);
    console.log(`To: ${config.actor}@company.com`);
}

async function main() {
    try {
        console.log('🤖 Starting Motivational Agent...');
        
        // Analyze the event and generate motivational content
        const motivationalContent = analyzeEventAndGenerateMessage();
        
        if (!motivationalContent.message) {
            console.log('No motivational message generated for this event type.');
            return;
        }
        
        console.log(`Generated message: ${motivationalContent.message}`);
        
        // Format message for Slack
        const slackMessage = formatSlackMessage(motivationalContent);
        
        // Send notifications
        await sendSlackNotification(slackMessage);
        
        // Optional: send email notification
        sendEmailNotification(motivationalContent);
        
        console.log('🎉 Motivational agent completed successfully!');
        
    } catch (error) {
        console.error('❌ Error in motivational agent:', error);
        process.exit(1);
    }
}

// Run the main function
main();