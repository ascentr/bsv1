//event listner for the click event on available class

const selectedData={}
var serviceSelected = false
var timeSelected = false
var confirmButtonCreated = false

document.querySelector('.slot').addEventListener('click', (e) =>{
  if (e.target.classList.contains('available')){
    handleSlot(e.target)
  }
})

document.getElementById('form').addEventListener('submit', submitData);

function handleClick(e) {
  // Get all elements with the class "store-item"
  const items = document.getElementsByClassName("service-item");

  // Deselect all items
  for (let item of items) {
      item.classList.remove("service-item-selected");
  }

  // Select the clicked item and update selectedData object
  e.classList.add("service-item-selected");

  service = {}
  service.name = e.dataset.name
  service.price = e.dataset.price
  service.slotsnumber = e.dataset.slotsnumber
  selectedData.service = service
  serviceSelected = true
  document.getElementById("times").scrollIntoView({ behavior: "smooth" });

}

function handleSlot(e) {
  if (e.classList.contains('booked')) return;

  if (serviceSelected == false ) {
    alert("Please Select A Service First")

    document.getElementById("services").scrollIntoView({ behavior: "smooth" });
    return
  }
  // Remove the 'available' class from the clicked element & add booked
  e.classList.remove('available');
  e.classList.add('booked');
  e.innerHTML = `<strong>${e.dataset.slot}</strong> - Booked`;
  timeSelected = true

  selectedData.slot = e.dataset.slot
  selectedData.date = e.dataset.date
  // Log the slot and date for confirmation
  document.getElementById('selected-details').innerHTML = 
    `<b>${selectedData.service.name}</b> booked for <br> Date: <b>${selectedData.date}</b><br>
      Time: <b>${selectedData.slot}</b>`
  // generateConfirmButton()
  showConfirmButton()
  document.getElementById("confirm").scrollIntoView({ behavior: "smooth" });
}

function showConfirmButton(){
  const div = document.getElementById('show-confirm')
  div.style.visibility = 'visible'
}

//Confirmation button is generated once the time slot(s) are selected.  
// The submitData() onclick event calls the submit data function that uses fetch API to send data
function generateConfirmButton(){
  if (confirmButtonCreated == false ){
      const confirmButton = document.createElement('button');
      confirmButton.textContent = "Confirm Booking";
      confirmButton.classList.add('btn')
      confirmButton.classList.add('btn-info')
      confirmButton.classList.add('btn-confirm')
      confirmButton.addEventListener("click", () => {
        submitData()
      })
      // confirmButton.onclick = submitData()
      document.getElementById('confirm-selected').appendChild(confirmButton);
      confirmButtonCreated = true;
      
    }
}

function submitData(event){
  event.preventDefault();
  const data = selectedData
    
  // console.log("data ==> ", data)
  // testDebugger();

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value; 
  url = "/bookings/create_booking/"
  fetch(url , {
    method : 'POST',
    headers : {
      'Content-Type' :'application/json',
      'X-CSRFToken': csrfToken
    },
    body : JSON.stringify(data)
  })
  .then(response => {
    if (response.ok){
      console.log("Success => ", data )
      return response.json();
    } else {
      throw new Error('Something Went Wrong')
    }
  })  
  .then(data => {
    console.log('Success:', data )
    location.reload(true);

  })
  .catch(error => {
    console.error('Error:', error)
    // testDebugger()
    // alert('Failed to create booking', error)
  });
  // window.location.href = window.location.href;
}

  // console.log('logging Data from submitData =>', data.service.name, data.service.price, data.date, data.slot, data.service.slotsnumber)

  function testDebugger() {
    console.log("Before debugger");
    debugger;
    console.log("After debugger");
}
