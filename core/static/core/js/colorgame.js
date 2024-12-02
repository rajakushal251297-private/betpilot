  // JavaScript functionality for the game
let selectedBall = 'None';
let timerInterval;

document.getElementById('myHistoryTab').addEventListener('click', function () {
    showTab('myHistory');
});

document.getElementById('previousResultsTab').addEventListener('click', function () {
    showTab('previousResults');
});

document.getElementById('previousHistoryTab').addEventListener('click', function () {
    showTab('previousHistory');
});

// Function to show the appropriate tab content
function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');

    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`.tab:contains(${tabId})`).classList.add('active');
    // document.querySelectorAll('.tab').forEach((element) => {
    //     if (element.textContent.includes(tabId)) {
    //         element.classList.add('active');
    //     }
    // });
}

// Function to handle ball selection
function selectBall(color) {
    selectedBall = color;
    document.getElementById('selected-ball').textContent ="You selected: " +color;
    document.getElementById('popup-selected-ball').textContent ="You selected: " +color;
    document.getElementById('bet-popup').style.display = 'block';
}

// Function to change bet amount
function changeAmount(direction) {
    const amountInput = document.getElementById('bet-amount');
    let currentAmount = parseInt(amountInput.value);
    currentAmount += direction;
    if (currentAmount >= 0) {
        amountInput.value = currentAmount;
        console.log('amount changed',currentAmount);
    }
}

// Function to confirm bet
function confirmBet() {
    let output = ''
    const amount = document.getElementById('bet-amount').value;
    console.log(selectedBall);
    const formdata = new FormData();
    if (parseInt(amount)>0){
        formdata.append('ballcolor',selectedBall)
        formdata.append('betamount',amount)
        fetch('/colorgame/',
            {
                method: 'POST',
                body: formdata
            }).then(response => response.json())
            .then(data => {
                if (data.status=='success'){
                console.log(data.ballcolorgamedata);
                for(var i=0; i<data.ballcolorgamedata.length; i++) {
                    output +='<tr>'+
                                '<td>'+data.ballcolorgamedata[i][0]+'</td>'+
                                '<td><span class="color-badge '+data.ballcolorgamedata[i][1]+'-ball"></span>'+ data.ballcolorgamedata[i][1]+'</td>'+
                                '<td>'+data.ballcolorgamedata[i][2]+'Rs.</td>'+
                            '</tr>'
                    

                }
                document.getElementById("previoushistoryid").innerHTML = output
                document.getElementById("balanceid").innerHTML = `Balance : ₹`+data.currentbalance
            }
            else{
                console.log(data)
                alert(data.status)
            }
            });
    }
    closePopup();
}

// Function to close the popup
function closePopup() {
    document.getElementById('bet-popup').style.display = 'none';
}

// Timer functionality
let timeremaining = document.getElementById('timeremaining').innerHTML
let totalTime = 120; // 2 minutes in seconds
const timerElement = document.getElementById('timer');

function startTimer() {
    console.log('start............')
    timerInterval = setInterval(() => {
        if (timeremaining <= 0) {
            clearInterval(timerInterval);
            timerElement.textContent = 120;
            console.log('time up............')
            timeremaining= 120
            startTimer()
            let output=''
            // let response = fetch("/updatedata/", {
            //     method: "GET"
            // })
            // console.log(response)
            
            fetch('/updatedata', {
                method: 'GET',
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    process_data(data,output);
                    console.log(data);
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
            
    

            timeremaining= 120
        }
        timeremaining--;
        const minutes = Math.floor(timeremaining / 60);
        const seconds = timeremaining % 60;
        timerElement.textContent = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }, 1000);
}

function process_data(data,output) {
    if (data.status=='success'){
        console.log(data.ballcolorgamedata);
        for(var i=0; i<data.ballcolorgamedata.length; i++) {
            console.log(data.ballcolorgamedata[i])
            output +='<tr>'+
                        '<td>'+data.ballcolorgamedata[i][0]+'</td>'+
                        '<td><span class="color-badge '+data.ballcolorgamedata[i][1]+'-ball"></span>'+ data.ballcolorgamedata[i][1]+'</td>'+
                        '<td>'+data.ballcolorgamedata[i][2]+'Rs.</td>'+
                    '</tr>'
            
        }
        document.getElementById("previoushistoryid").innerHTML = output
        document.getElementById("balanceid").innerHTML = `Balance : ₹`+data.currentbalance
        output=''
        for(var i=0; i<data.allwinrecord_lst.length; i++) {
            const timestamp = data.allwinrecord_lst[i][0];
            const date = new Date(timestamp);
            const options = { 
                hour: 'numeric', 
                minute: 'numeric', 
                hour12: true, 
                month: 'long', 
                day: 'numeric', 
                year: 'numeric' 
            };
            const formattedDate = date.toLocaleString('en-US', options);
            output +='<tr>'+
                        '<td>'+formattedDate.replace("at ",",")+'</td>'+
                        '<td><span class="color-badge '+data.allwinrecord_lst[i][1]+'-ball"></span>'+ data.allwinrecord_lst[i][1]+'</td>'+
                        '<td>'+data.allwinrecord_lst[i][2]+'Rs.</td>'+
                    '</tr>'
            

        }
        document.getElementById("userhistoryid").innerHTML = output
        output=''
        for(var i=0; i<data.previous_history.length; i++) {
            const timestamp = data.previous_history[i][0];
            const date = new Date(timestamp);
            const options = { 
                hour: 'numeric', 
                minute: 'numeric', 
                hour12: true, 
                month: 'long', 
                day: 'numeric', 
                year: 'numeric' 
            };
            const formattedDate = date.toLocaleString('en-US', options);
            output +='<tr>'+
                        '<td>'+formattedDate.replace("at ",",")+'</td>'+
                        '<td><span class="color-badge '+data.previous_history[i][1]+'-ball"></span>'+ data.previous_history[i][1]+'</td>'+
                    '</tr>'
            

        }
        document.getElementById("allprevioushistoryid").innerHTML = output
        
    }
    else{
        alert(data.status)
    }
}
// Start the timer when the page loads

window.onload = startTimer;



