export default {
    ERROR_MEMO: {
        link_id: -1,
        title: 'unknown',
        description: 'unknown',
        platforms: [],
        million: false,
        createAt: null
    },
    NEW_EMPTY_MEMO() {
        return {
            description: '',
            createAt: null,
            photoURL: ''
        }
    },
    PLATFORMS: ['FC', 'SFC', 'GB', '64', 'GC', 'DS', 'Wii', '3DS', 'Wii U', 'Switch'],
    SLACK_SERVER_ERROR: 'https://hooks.slack.com/services/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',
    GENERATE_URL: 'https://aitter-twigene.work/generate',
    TWEET_URL: 'https://aitter-twigene.work/tweet'
}