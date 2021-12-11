console.log("here")

axios.get("http://192.168.0.156:7542/")
  .then((response) => {
    console.log(response);
  }, (error) => {
    console.log(error);
  });
