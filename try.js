

axios.get("https://processdatawithk.herokuapp.com/access/admin/signup/a/a")
  .then((response) => {
    console.log(response);
    console.log("here")
  }, (error) => {
    console.log(error);
  });
