document.addEventListener('DOMContentLoaded', () => {
    const games = [
        {
            name: 'Poker',
            contests: [
                { name: 'Contest 1', info: 'Buy-in: $100, Prize: $1000', status: 'Ongoing' },
                { name: 'Contest 2', info: 'Buy-in: $50, Prize: $500', status: 'Finished' },
                { name: 'Contest 3', info: 'Buy-in: $200, Prize: $2000', status: 'Ongoing' }
            ]
        },
        {
            name: 'Blackjack',
            contests: [
                { name: 'Contest A', info: 'Buy-in: $70, Prize: $700', status: 'Finished' },
                { name: 'Contest B', info: 'Buy-in: $30, Prize: $300', status: 'Ongoing' }
            ]
        },
        {
            name: 'Roulette',
            contests: [
                { name: 'Contest X', info: 'Buy-in: $20, Prize: $200', status: 'Ongoing' },
                { name: 'Contest Y', info: 'Buy-in: $100, Prize: $1000', status: 'Finished' },
                { name: 'Contest Z', info: 'Buy-in: $50, Prize: $500', status: 'Ongoing' }
            ]
        }
    ];

    const gamesSection = document.getElementById('games-section');

    games.forEach(game => {
        // Create game title
        const gameTitle = document.createElement('div');
        gameTitle.classList.add('game-title');
        gameTitle.innerHTML = `${game.name} <span class="icon">▼</span>`;

        // Create expandable game contest section
        const gameContests = document.createElement('div');
        gameContests.classList.add('game-contests');

        game.contests.forEach(contest => {
            // Create contest item
            const contestItem = document.createElement('div');
            contestItem.classList.add('contest-item');

            // Contest info and status
            const contestInfo = document.createElement('div');
            contestInfo.classList.add('contest-info');
            contestInfo.innerHTML = `<strong>${contest.name}</strong><br>${contest.info}`;

            const contestStatus = document.createElement('div');
            contestStatus.classList.add('contest-status');
            contestStatus.textContent = contest.status;

            contestItem.appendChild(contestInfo);
            contestItem.appendChild(contestStatus);
            gameContests.appendChild(contestItem);
        });

        // Toggle expand/collapse on click
        gameTitle.addEventListener('click', () => {
            gameTitle.classList.toggle('expanded');
            gameContests.style.maxHeight = gameContests.style.maxHeight === '500px' ? '0' : '500px';
        });

        gamesSection.appendChild(gameTitle);
        gamesSection.appendChild(gameContests);
    });
});
