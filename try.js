console.log("here")

axios.get("https://processdatawithk.herokuapp.com/table/2/3/4")
  .then((response) => {
    console.log(response);
  }, (error) => {
    console.log(error);
  });
