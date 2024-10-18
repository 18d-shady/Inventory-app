// Get all edit buttons
const editBtns = document.querySelectorAll('.edit-btn');
const deleteBtns = document.querySelectorAll('.delete-btn');

deleteBtns.forEach((btn) => {
  btn.addEventListener('click', function() {
	const rowId = this.id;
    var formData = new FormData();
	formData.append("row_id", rowId);

	fetch("/delete-product", {
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

// Add event listener to each edit button
editBtns.forEach((btn) => {
  btn.addEventListener('click', function() {
	const rowId = this.id;
    const row = document.getElementById(`row-${rowId}`);
    //console.log(row);

    let nameValue = row.cells[2].textContent;
    let imageValue = row.cells[1].textContent;
    let codeValue = row.cells[3].textContent;
    let brandValue = row.cells[4].textContent;
    let quantityValue = row.cells[5].textContent;
    let priceValue = row.cells[6].textContent;
	console.log(nameValue, codeValue, quantityValue);

    // Remove the row
    row.remove();

    // Create a new row with input fields
    var newRows = document.createElement('tr');
    
    newRows.innerHTML = `

      	<td class="py-1">${rowId}</td>
	    <td><input type="file" class="form-control w-10 text-sm" id="product-image" value="${imageValue}" accept="image/*"></td>
	    <td><input type="text" class="form-control w-10 text-sm" id="product-name" value="${nameValue}"></td>
	    <td><input type="text" class="form-control w-9 text-sm" id="product-code" value="${codeValue}"></td>
	    <td><input type="text" class="form-control w-10 text-sm" id="product-brand" value="${brandValue}"></td>
	    <td><input type="number" class="form-control w-10 text-sm" id="product-quantity" value="${quantityValue}"></td>
	    <td><input type="number" class="form-control w-10 text-sm" id="product-price" value="${priceValue}"></td>
	    <td>
	    	<button class="bg-blue-900 text-white p-1 rounded-md done-btn">
				<svg class="h-5 w-5"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M5 12l5 5l10 -10" />
				</svg>
			</button>
			<button class="bg-red-600 text-white p-1 rounded-md remove-btn">
				<svg class="h-5 w-5"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <line x1="4" y1="7" x2="20" y2="7" />  <line x1="10" y1="11" x2="10" y2="17" />  <line x1="14" y1="11" x2="14" y2="17" />  <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />  <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
				</svg>
			</button>

	    </td>
	  
    `;
    
    document.getElementById("table-body").appendChild(newRows);

  // Add event listener to the save button
  var doneBtn = newRows.querySelector(".done-btn");
	  doneBtn.addEventListener("click", function() {
	// Get the values from the input fields
	var productName = newRows.querySelector("#product-name").value;
    var productImage = newRows.querySelector("#product-image");
    var productCode = newRows.querySelector("#product-code").value;
    var productBrand = newRows.querySelector("#product-brand").value;
    var productQuantity = newRows.querySelector("#product-quantity").value;
    var productPrice = newRows.querySelector("#product-price").value;

	

	// Create a new form data object
	var formData = new FormData();
	formData.append("row_id", rowId);
	formData.append("product_name", productName);
	formData.append("product_image", productImage.files[0]);
	formData.append("product_code", productCode);
	formData.append("product_brand", productBrand);
	formData.append("product_quantity", productQuantity);
	formData.append("product_price", productPrice);

	// Send the data to the server using fetch API
	fetch("/update-product", {
	method: "POST",
	body: formData
	})
	.then(response => response.json())
	//.then(data => console.log(data))
	.then(data => {
		if (data.message) {
	    location.reload();
	  } 
	})
	.catch(error => console.error(error));

	// Remove the new row from the table
	newRows.remove();
	//location.reload();
  });

  var removeBtn = newRows.querySelector(".remove-btn");
  removeBtn.addEventListener("click", function() {
    newRows.remove();
  });

  });
});


document.getElementById("add-product-btn").addEventListener("click", function() {
  var newRow = document.createElement("tr");
  newRow.innerHTML = `
    <td><input type="text" class="form-control w-7 text-sm" id="product-serial-number" placeholder="S/N"></td>
    <td><input type="file" class="form-control w-10 text-sm" id="product-image" accept="image/*" placeholder="Image"></td>
    <td><input type="text" class="form-control w-10 text-sm" id="product-name" placeholder="Name"></td>
    <td><input type="text" class="form-control w-9 text-sm" id="product-code" placeholder="Code"></td>
    <td><input type="text" class="form-control w-10 text-sm" id="product-brand" placeholder="Brand"></td>
    <td><input type="number" class="form-control w-10 text-sm" id="product-quantity" placeholder="Quantity"></td>
    <td><input type="number" class="form-control w-10 text-sm" id="product-price" placeholder="Price"></td>
    <td>
    	<button class="bg-blue-900 text-white p-1 rounded-md save-btn">
			<svg class="h-5 w-5"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <path d="M5 12l5 5l10 -10" />
			</svg>
		</button>
		<button class="bg-red-600 text-white p-1 rounded-md cancel-btn">
			<svg class="h-5 w-5"  width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">  <path stroke="none" d="M0 0h24v24H0z"/>  <line x1="4" y1="7" x2="20" y2="7" />  <line x1="10" y1="11" x2="10" y2="17" />  <line x1="14" y1="11" x2="14" y2="17" />  <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12" />  <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3" />
			</svg>
		</button>

    </td>
  `;
  document.getElementById("table-body").appendChild(newRow);

  // Add event listener to the save button
  var saveBtn = newRow.querySelector(".save-btn");
	  saveBtn.addEventListener("click", function() {
	// Get the values from the input fields
	var productName = newRow.querySelector("#product-name").value;
    var productImage = newRow.querySelector("#product-image");
    var productCode = newRow.querySelector("#product-code").value;
    var productBrand = newRow.querySelector("#product-brand").value;
    var productQuantity = newRow.querySelector("#product-quantity").value;
    var productPrice = newRow.querySelector("#product-price").value;

	

	// Create a new form data object
	var formData = new FormData();
	formData.append("product_name", productName);
	formData.append("product_image", productImage.files[0]);
	formData.append("product_code", productCode);
	formData.append("product_brand", productBrand);
	formData.append("product_quantity", productQuantity);
	formData.append("product_price", productPrice);

	// Send the data to the server using fetch API
	fetch("/add-product", {
	method: "POST",
	body: formData
	})
	.then(response => response.json())
	//.then(data => console.log(data))
	.then(data => {
		if (data.message) {
	    location.reload();
	  } 
	})
	.catch(error => console.error(error));

	// Remove the new row from the table
	newRow.remove();
	//location.reload();
  });
  

  var cancelBtn = newRow.querySelector(".cancel-btn");
  cancelBtn.addEventListener("click", function() {
    newRow.remove();
  });
});

// Get the print button and table elements
const printButton = document.getElementById('printButton');
const table = document.getElementById('product-table');

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