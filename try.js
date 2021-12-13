

axios.get("https://processdatawithk.herokuapp.com/access/guest/signup/a/a")
  .then((response) => {
    console.log(response);
    console.log("here")
  }, (error) => {
    console.log(error);
  });
