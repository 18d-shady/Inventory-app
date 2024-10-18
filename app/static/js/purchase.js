// Get all edit buttons
const editBtns = document.querySelectorAll('.edit-btn');
const deleteBtns = document.querySelectorAll('.delete-btn');

deleteBtns.forEach((btn) => {
  btn.addEventListener('click', function() {
	const rowId = this.id;
    var formData = new FormData();
	formData.append("row_id", rowId);

	fetch("/delete-purchase", {
	method: "POST",
	body: formData
	})
	.then(response => response.json())
	.then(data => {
		if (data.message) {
	    location.reload();
	  } 
	
	})
	.catch(error => console.error(error));

	// Remove the new row from the table

	//location.reload();

    
  });
});

document.addEventListener("DOMContentLoaded", function() {
  const viewItemsButtons = document.querySelectorAll("button[id^='view-items-']");

  viewItemsButtons.forEach(function(button) {
      button.addEventListener("click", function() {
          const purchaseId = button.id.replace("view-items-", "");
          const xhr = new XMLHttpRequest();
          xhr.open('GET', `/get_purchase_items/${purchaseId}`, true);
          xhr.onload = function() {
              if (xhr.status === 200) {
                  const purchaseItems = JSON.parse(xhr.responseText);
                  const additionalItemsContainer = document.getElementById(`additional-items-${purchaseId}`);
                  const html = purchaseItems.map(item => `<li>${item.name} x ${item.quantity}</li>`).join('');
                  additionalItemsContainer.innerHTML = html;
                  additionalItemsContainer.classList.toggle("hidden");
              }
          };
          xhr.send();
      });
  });
});



document.getElementById("add-purchase-btn").addEventListener("click", function() {
  var div = document.getElementById("add-purchase-div");
    if (div.style.display === "none") {
        div.style.display = "block";
    } else {
        div.style.display = "none";
    }
});

let valuesArray = [];

function addProducts(){
	const selectElement = document.getElementById("product-name");
  const selectValue = selectElement.value;
  const selectText = selectElement.options[selectElement.selectedIndex].text;
  const numberValue = document.getElementById("product-quantity").value;

  //valuesArray.push({ selectValue, numberValue, selectText });
  valuesArray.push({ selectValue, numberValue });
  document.getElementById("resultDiv").innerHTML += `<p>${selectText}  x${numberValue}</p>`;

}

function sendValuesToFlask() {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/add-purchase", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onload = function() {
		    if (xhr.status === 200) {
		        // Request was successful, reload the page
		        window.location.reload();
		    } else {
		        // Request failed, handle the error
		        console.error("Error:", xhr.statusText);
		    }
		};
    xhr.send(JSON.stringify(valuesArray));
}

// Get the print button and table elements
const printButton = document.getElementById('printButton2');
const table = document.getElementById('purchase-table');

// Add an event listener to the print button
printButton.addEventListener('click', () => {
  // Create a new window for printing
  const printWindow = window.open('', '_blank');

  // Create a new HTML document for printing
  const printDoc = printWindow.document;

  // Add the table to the print document
  printDoc.write('<html><head><title>Print Table</title></head><body>');
  printDoc.write(table.outerHTML);
  printDoc.write('</body></html>');

  // Style the print output using CSS
  printDoc.write('<style>table { border-collapse: collapse; } th, td { border: 1px solid #ddd; padding: 8px; }</style>');

  // Print the document
  printWindow.print();

  // Close the print window
  printWindow.close();
});
