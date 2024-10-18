var date = new Date();
var previousMonth = date.toLocaleString("en-US", { month: "long" });
previousMonth = new Date(date.getFullYear(), date.getMonth() - 1).toLocaleString("en-US", { month: "long" });
document.getElementById("dpreviousMonth").innerText = previousMonth;
document.getElementById("dpreviousMonth2").innerText = previousMonth;

const stockButton = document.getElementById('lowStock');
stockButton.addEventListener('click', () => {
  const xhr = new XMLHttpRequest();
  xhr.open('GET', `/get_low_stock`, true);
  xhr.onload = function() {
      if (xhr.status === 200) {
          const lowStockItems = JSON.parse(xhr.responseText);
          const additionalItemsContainer = document.getElementById(`additional-items`);
          const lowContainer = document.getElementById(`low-items`);
          const html = lowStockItems.map(item => `<li>
            Product Number ${item.product_id} - ${item.name},
            Quantity: ${item.quantity} 
            </li><hr>`).join('');
          lowContainer.innerHTML = html;
          additionalItemsContainer.classList.toggle("hidden");
      }
  };
  xhr.send();
})


const ctx = document.getElementById('salesChart').getContext('2d');
  fetch('/fill_chart')
      .then(response => response.json())
      .then(data => {
          new Chart(ctx, {
              type: 'line',
              data: data,
              options: {
                  title: {
                      display: true,
                      text: 'Sales in the last 7 days'
                  }
              }
          });
      });


  // Get the print button and table elements
  const printButton = document.getElementById('printButton');
  const table = document.getElementById('main');

  // Add an event listener to the print button
  printButton.addEventListener('click', () => {
    // Create a new window for printing
    const printWindow = window.open('', '_blank');

    // Create a new HTML document for printing
    const printDoc = printWindow.document;

    // Add the table to the print document
    printDoc.write('<html><head><title>Print Table</title></head><body>');
    printDoc.write(table.outerHTML);
    printDoc.write(ctx);
    printDoc.write('</body></html>');

    // Style the print output using CSS
    printDoc.write('<style> div { border: 1px solid #ddd; padding: 8px; }</style>');
    // Get the canvas element

    // Print the document
    printWindow.print();

    // Close the print window
    printWindow.close();
  });

  /*
  const xValues = [50,60,70,80,90,100,110,120,130,140,150];
  const yValues = [7,8,8,9,9,9,10,11,14,14,15];

  new Chart("salesChart", {
    type: "line",
    data: {
      labels: xValues,
      datasets: [{
        fill: false,
        lineTension: 0,
        backgroundColor: "rgba(0,0,255,1.0)",
        borderColor: "rgba(0,0,255,0.1)",
        data: yValues
      }]
    },
    options: {
      legend: {display: false},
      scales: {
        yAxes: [{ticks: {min: 6, max:16}}],
      }
    }
  });
  */