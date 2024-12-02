document.addEventListener('DOMContentLoaded', () => {
    const buttons = document.querySelectorAll('.join-btn');
    const participantCounts = {
        'contest-1': 0,
        'contest-2': 0,
        'contest-3': 0,
    };

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            const contestId = button.getAttribute('data-contest');
            if (participantCounts[contestId] < 10) {
                participantCounts[contestId]++;
                const progressBar = document.getElementById(`progress-${contestId.split('-')[1]}`);
                const percentage = (participantCounts[contestId] / 10) * 100;
                progressBar.style.width = percentage + '%';

                //alert(`You joined ${contestId.replace('-', ' ')}. Participants: ${participantCounts[contestId]}/10`);
            } else {
                alert('This contest is already full!');
            }
        });
    });
});
