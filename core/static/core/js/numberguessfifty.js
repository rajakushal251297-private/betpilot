document.addEventListener('DOMContentLoaded', () => {
    const numberGrid = document.querySelector('.number-grid');
    const selectedNumberDisplay = document.getElementById('selected-number');
    const playButton = document.getElementById('play-button');
    let selectedNumber = null;

    // Create buttons for numbers 0-9
    for (let i = 0; i <= 9; i++) {
        const button = document.createElement('button');
        button.classList.add('number-button');
        button.textContent = i;

        // Add click event listener
        button.addEventListener('click', () => {
            selectedNumber = i;
            selectedNumberDisplay.textContent = "You selected: "+selectedNumber;
            highlightSelectedButton(button);
        });

        numberGrid.appendChild(button);
    }

    // Play button event listener
    playButton.addEventListener('click', () => {
        if (selectedNumber !== null) {
            selectedNumberDisplay.textContent = "You selected: "+selectedNumber;
            selectedButtonFunction(selectedNumber)
        } else {
            selectedNumberDisplay.textContent = 'Please select number!';
        }
    });

    // Function to highlight the selected button
    function highlightSelectedButton(selectedButton) {
        // Remove 'selected' class from all buttons
        const allButtons = document.querySelectorAll('.number-button');
        allButtons.forEach(btn => btn.classList.remove('selected'));
        
        // Add 'selected' class to the clicked button
        selectedButton.classList.add('selected');
    }
});


function selectedButtonFunction(selectbutton) {
    const formdata = new FormData();
    formdata.append("selectednumber", selectbutton);
    
    fetch("/numberguessfifty/", {
        method: "POST",
        body: formdata
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.remaining_balance);
        document.getElementById("total_amount_id").innerHTML = "💰 " + data.remaining_balance;
        
        let output = "";
        if(data.status == "true") {
        for (let i = 0; i < data.my_history.length; i++) { // Correct loop condition
            let mydata = data.my_history[i];
            console.log(mydata[1]);
            let dt = mydata[0]; // Simplified indexing
            let num = mydata[1];
            output += "<tr><td>" + dt + "</td><td>" + num + "</td><td>50</td></tr>"; // Corrected <td> closure
        }
        
        document.getElementById("my_history_id").innerHTML = output;
        }   
        else {
            alert(data.message);
        }
    })
    .catch(error => console.error("Error:", error)); // Added error handling
}
