
function add(event){
 
  axios.post('http://127.0.0.1:5000/', {
    org : document.getElementById('o').value,
    domain : document.getElementById('d').value,
    purpose : document.getElementById('p').value,
    country : document.getElementById('c').value
  })
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
}

function del(){
  axios.delete('http://127.0.0.1:5000/' + document.getElementById('del').value)
  .then(function (response) {
    console.log(response);
  })
  .catch(function (error) {
    console.log(error);
  });
}