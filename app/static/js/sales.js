document.addEventListener("DOMContentLoaded", function() {
  const viewItemsButtons = document.querySelectorAll("button[id^='view-items-']");

  viewItemsButtons.forEach(function(button) {
      button.addEventListener("click", function() {
          const salesId = button.id.replace("view-items-", "");
          const xhr = new XMLHttpRequest();
          xhr.open('GET', `/get_sales_items/${salesId}`, true);
          xhr.onload = function() {
              if (xhr.status === 200) {
                  const salesItems = JSON.parse(xhr.responseText);
                  const additionalItemsContainer = document.getElementById(`additional-items-${salesId}`);
                  const html = salesItems.map(item => `<li>Time Bought: ${item.time_bought}, 
                  	Quantity: ${item.quantity}, 
                  	Total Price: ${item.total_price}
                  	<br>
                   <span>Items bought: ${item.description}</span></li><hr>`).join('');
                  additionalItemsContainer.innerHTML = html;
                  additionalItemsContainer.classList.toggle("hidden");
              }
          };
          xhr.send();
      });
  });
});

// Get the print button and table elements
const printButton = document.getElementById('printButton');
const table = document.getElementById('sales-table');

// Add an event listener to the print button
printButton.addEventListener('click', function() {
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