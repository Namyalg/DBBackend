console.log("here")

axios.get("https://processdatawithk.herokuapp.com/access/guest/signup/a/a")
  .then((response) => {
    console.log(response);
  }, (error) => {
    console.log(error);
  });
