const dateTimeElement = document.getElementById('date-time');

function updateDateTime() {
    const now = new Date();
    const formattedDateTime = now.toLocaleString();
    dateTimeElement.innerText = formattedDateTime;
}

updateDateTime();
setInterval(updateDateTime, 1000);


const clickableDivs = document.querySelectorAll('.clickable-div');
  const displayedTextContainer = document.getElementById('resultDiv');

  clickableDivs.forEach((div) => {
    div.addEventListener('click', () => {
      const childId = div.querySelector('h3').textContent;
      const childPrice = div.querySelector('h3').id;
      const childText = div.querySelector('h4').textContent;
      const displayedTextHtml = `
        <div class="cartItem">
        	<h3 class="hidden">${childPrice}</h3>
          <p id="${childId}" class="inline-block">${childText}</p>
          <input type="number" value="0" id="${childId}-input" class="add-allP inline-block w-10 float-right">
        </div>
      `;
      displayedTextContainer.innerHTML += displayedTextHtml;

      // Add event listener to update input value in real-time

      const inputField = document.getElementById(`${childId}-input`);
      inputField.addEventListener('input', () => {
        const updatedValue = inputField.value;
        // You can send the updated value to Flask here
        console.log(`Updated value for ${childId}: ${updatedValue}`);
      });

      const inputClass = document.querySelectorAll('.add-allP');
			const totalItems = document.getElementById('totalItems');
			inputClass.forEach((input) => {
			  input.addEventListener('input', function() {
			    let sum = 0;
			    inputClass.forEach((input) => {
			      sum += parseInt(input.value) || 0;
			    });
			    totalItems.innerText = `Total Items: ${sum}`;
			  });
			});

			const priceList = document.querySelectorAll('.cartItem');
			const totalAmount = document.getElementById('totalAmount');
			console.log(priceList)
			let total_price = 0;

			// Function to calculate the total price
			function calculateTotalPrice() {
			  total_prices = 0;
			  priceList.forEach((divss) => {
			    const className = divss.querySelector('h3').textContent;
			    const number = parseInt(className);
			    const input = divss.querySelector('input');
			    const inputValue = parseInt(input.value);
			    const result = number * inputValue;
			    total_prices += result;
			  });
			  totalAmount.innerText = `Total Amount: N${total_prices}`;
			  console.log(`The sum is: ${total_prices}`);
			}

			// Add event listeners to each input field
			priceList.forEach((divss) => {
			  const input = divss.querySelector('input');
			  input.addEventListener('input', calculateTotalPrice);
			});

			// Initial calculation
			calculateTotalPrice();

    });
  });

  // Send all displayed text and input values to Flask
  
function sendData() {
  const quantity = document.getElementById('totalItems').textContent;
  const total_price = document.getElementById('totalAmount').textContent;
  const displayedTextData = [];

  const displayedTextElements = displayedTextContainer.children;
  Array.from(displayedTextElements).forEach((element) => {
    const childText = element.querySelector('p').id;
    const inputValue = element.querySelector('input').value;
    displayedTextData.push({ childText, inputValue });
  });

  const dataToSend = {
    quantity: quantity,
    total_price: total_price,
    displayedTextData: displayedTextData
  };

  console.log('Sending data:', dataToSend);

  // Send the data to Flask using XMLHttpRequest
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/new-sales', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onload = function() {
	    if (xhr.status === 200) {
	        // Request was successful, reload the page
	        window.location.reload();
	    } else {
	        // Request failed, handle the error
	        console.error("Error:", xhr.statusText);
	    }
	};
  xhr.send(JSON.stringify(dataToSend));
}



